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
def packet_handler(packet):
    if packet.haslayer(scapy.Dot11):
        if packet.haslayer(scapy.Dot11Beacon):
            ssid = packet[scapy.Dot11Elt].info.decode(errors='ignore')
            bssid = packet[scapy.Dot11].addr2
            channel = packet[scapy.Dot11Elt:3].info
            channel = int.from_bytes(channel, byteorder='little')
            privacy = packet[scapy.Dot11Elt:4].info
            privacy = int(privacy[1])
            ssid.replace("\0", "")
            ssid.replace("\x00", "")
            if channel > 13:
                ssid = f"(5G) {ssid}"
            with globals.lock:
                if bssid not in bssids:
                    bssids.append(bssid)
                    ssids.append(ssid)
                    channels.append(channel)
                    sec.append(get_sec(privacy))
                
def find_clients(packet):
    if packet.haslayer(scapy.Dot11):
        target = globals.selected_bssid
        addrs = [packet.addr1, packet.addr2, packet.addr3]
        if target in addrs:
            for addr in addrs:
                if addr and addr != target and addr != "ff:ff:ff:ff:ff:ff":
                    with globals.lock:
                        if addr not in clients:
                            clients.append(addr)
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
        CHANNELS= [1, 2, 3, 4, 
                         5, 6, 7, 8, 
                         9, 10, 11, 12, 
                         13, 36, 40, 44, 48,           # UNII-1
                        52, 56, 60, 64,           # UNII-2A
                        100, 104, 108, 112, 116,   # UNII-2C
                        120, 124, 128, 132, 136, 
                        140, 144,
                        149, 153, 157, 161, 165   # UNII-3
                        ]
        return random.choice(CHANNELS)
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
            else:
                time.sleep(0.5)
    def continuous_running(self):
        probe_thread = threading.Thread(target=self.send_probe_request, daemon=True)
        scans_before_reset = 5
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
                        scapy.sniff(filter=f" wlan host {globals.selected_bssid}", iface=globals.interface, prn=find_clients, store=0, timeout=1,stop_filter=lambda x: not globals.stop_scan)
                    scans_before_reset -= 1 
                    if scans_before_reset <= 0:
                        if not globals.stop_scan:
                            globals.l_bssids = bssids.copy()
                            globals.l_ssids = ssids.copy()
                            globals.l_sec = sec.copy()
                            globals.l_channels = channels.copy()
                            channels.clear()
                            bssids.clear()
                            ssids.clear()
                            sec.clear()
                        else:
                            globals.clients = clients.copy()
                            clients.clear()
                        
                        scans_before_reset = 5
                else:
                    time.sleep(1)
            except Exception as e:
                print(f"Error occurred: {e}")
                time.sleep(1)
