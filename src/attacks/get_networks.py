import csv
import random
import subprocess
import os
import time
import globals
import threading
import scapy.all as scapy

ssids = []
bssids = []
sec = []
channels = []
clients = []
def get_sec(priv):
    if priv == 0:
        return "OPEN"
    elif priv == 1:
        return "WEP"
    elif priv == 2:
        return "WPA"
    elif priv == 3:
        return "WPA2"
    else:
        return "UNKNOWN"
scans_before_reset = 10
def packet_handler(packet):
    global scans_before_reset
    if packet.haslayer(scapy.Dot11):
        if packet.haslayer(scapy.Dot11Beacon):
            ssid = packet[scapy.Dot11Elt].info.decode(errors='ignore')
            bssid = packet[scapy.Dot11].addr2
            channel = packet[scapy.Dot11Elt:3].info
            channel = int.from_bytes(channel, byteorder='little')
            privacy = packet[scapy.Dot11Elt:4].info
            privacy = int(privacy[1])
            with globals.lock:
                if bssid not in bssids:
                    bssids.append(bssid)
                    ssids.append(ssid)
                    channels.append(channel)
                    sec.append(get_sec(privacy))
                scans_before_reset -= 1   
                if scans_before_reset <= 0:
                    globals.l_bssids = bssids
                    globals.l_ssids = ssids
                    globals.l_sec = sec
                    globals.l_channels = channels
                    globals.clients = clients
                    bssids.clear()
                    ssids.clear()
                    sec.clear()
                    channels.clear()
                    clients.clear()
                    scans_before_reset = 10
def find_clients(packet):
    if packet.haslayer(scapy.Dot11):
        if packet.addr1 == globals.selected_bssid or packet.addr2 == globals.selected_bssid:
            client_mac = packet.addr1 if packet.addr1 != globals.selected_bssid else packet.addr2
            with globals.lock:
                if client_mac not in clients:
                    clients.append(client_mac)
def selected_network_info():
    with globals.lock:
        if globals.selected_bssid:
            return True
        return False
class get_networks: 
    def __init__(self):
        self._event_stop = threading.Event()
    def stop(self):
        self._event_stop.set()
    def change_channel(self):
        if globals.current_channel < 11:
            globals.current_channel += 1
        else:
            globals.current_channel = 1
    def send_probe_request(self):
        while not self._event_stop.is_set():
            if not globals.stop_scan:
                random_mac = scapy.RandMAC()
                self.change_channel()
                try:
                    subprocess.run(
                        ["sudo", "iw", "dev", globals.interface, "set", "channel", str(globals.current_channel)],
                        check=True,
                        capture_output=True,
                        text=True
                    )
                except subprocess.CalledProcessError as e:
                    print(f"Failed to set channel to {globals.current_channel}: {e.stderr}")
                probe_p = scapy.RadioTap() / scapy.Dot11(addr1="ff:ff:ff:ff:ff:ff",  
                                    addr2=random_mac,
                                    addr3="ff:ff:ff:ff:ff:ff") / scapy.Dot11ProbeReq()
                scapy.sendp(probe_p, iface=globals.interface, count = 3, inter = 0.1, verbose=False)
    def continuous_running(self):
        probe_thread = threading.Thread(target=self.send_probe_request, daemon=True)
        while not self._event_stop.is_set():
            try:
                if not globals.send_beacon:
                    if not globals.stop_scan:
                        if not probe_thread.is_alive():
                            probe_thread.start()
                        scapy.sniff(iface=globals.interface, prn=packet_handler, store=0, timeout = 2,stop_filter=lambda x: selected_network_info())
                        globals.set_and_calc_networks()
                        if globals.fix:
                            globals.csv_saver.log()
                    elif globals.stop_scan and globals.selected_bssid:
                        if globals.current_channel != globals.channel:
                            subprocess.run(["sudo", "iw", "dev", globals.interface, "set", "channel", str(globals.channel)], check=True)
                            globals.current_channel = globals.channel
                        scapy.sniff(filter=f" wlan host {globals.selected_bssid}", iface=globals.interface, prn=find_clients, store=0, stop_filter=lambda x: not globals.stop_scan)
                    
                else:
                    time.sleep(1)
            except Exception as e:
                print(f"Error occurred: {e}")
                time.sleep(1)
