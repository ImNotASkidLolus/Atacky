import scapy.all as scapy
import globals
import time 
import threading
import subprocess

class BeaconSpam:
    def __init__(self):
        self.IFACE = globals.interface
        self._stop_event = threading.Event()
        self.channel = 1
        self.counter = 1
        self.start_time = 0
    def stop(self):
        self._stop_event.set()
    def build_beacon_packet(self,ssid:str, channel):
        ts = (time.time_ns() - self.start_time)//1000
        rand_mac = str(scapy.RandMAC())
        packet = (
            scapy.RadioTap()/
            scapy.Dot11(type=0, subtype=8,
                addr1='ff:ff:ff:ff:ff:ff',  # Broadcast
                addr2=rand_mac,
                addr3=rand_mac) /
            scapy.Dot11Beacon(timestamp= ts, beacon_interval = 1000, cap=0x31)/
            scapy.Dot11Elt(ID='SSID', info=str(ssid), len=len(ssid))/
            scapy.Dot11Elt(ID= 3, info=(bytes([channel])))/ #set the channel
            scapy.Dot11Elt(ID='Rates', info=b'\x82\x84\x8b\x96\x0c\x12\x18\x24') / # supported rates
            scapy.Dot11Elt(ID='RSNinfo', info=( #RSN info
                b'\x01\x00'
                b'\x00\x0f\xac\x04'
                b'\x02\x00'
                b'\x00\x0f\xac\x04'
                b'\x00\x0f\xac\x02'
                b'\x01\x00'
                b'\x00\x0f\xac\x02'
                b'\x00\x00'))
        )
        return packet
    def next_channel(self):
        if self.channel < 13:
            self.channel+=1
            try:
                subprocess.run(["iw", "dev", self.IFACE, "set", "channel", str(self.channel)], check=True)
            except Exception as e:
                print(f"Failed to set channel via iw: {e}")
        else:
            self.channel = 1
    def start_beacon_spam(self):
        self.start_time = time.time_ns()
        self.next_channel()
        while not self._stop_event.is_set() and not globals.larp_mode:
            try:
                ssid = globals.selected_ssid + str(self.counter)
                self.counter +=1
                if self.counter > 9999:
                    self.next_channel()
                    self.counter = 1
                pkt = self.build_beacon_packet(ssid, self.channel)
                for i in range(2):
                    scapy.sendp(pkt, iface=self.IFACE, verbose=False, inter=0.1)
                globals.bc += 1
            except Exception as e:
                print(e)
                time.sleep(0.1)                