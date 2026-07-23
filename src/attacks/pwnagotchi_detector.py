import globals
import scapy.all as scapy
import threading
import os
import json

class pwngrid_detect:
    def __init__(self):
        self._stop = threading.Event()
        self.found_pwnagotchi = False
        self.pwnagotchis_found = []
    def stop(self):
        self._stop.set()
    def reset(self):
        self._stop = threading.Event()
    def check_for_pwnagotchi(self,packet:scapy.packet):
        if packet.haslayer("Dot11Beacon"):
            addr1 = packet.addr1
            addr2 = packet.addr2
            addr3 = packet.addr3
            if "de:ad:be:ef:de:ad" in (addr1, addr2, addr3):
                try:
                    info_layer = packet.getlayer("Dot11Elt")
                    if info_layer:
                        raw_info = info_layer.info.decode('utf-8', errors='ignore')
                        data = json.loads(raw_info)
                        self.pwnagotchis_found.append(data)
                except Exception as e:
                    print(f"ERROR in pwnagotchi checker: {e}")
    def pwnagotchi_finder(self):
        while not self._stop.is_set():
            scapy.sniff(iface=globals.interface, prn=self.check_for_pwnagotchi)
