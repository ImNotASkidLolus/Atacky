import scapy.all as scapy
import globals
import threading
import time



class capture:
    def __init__(self):
        self._stop = threading.Event()
        self.file = "capture.pcap"
        self.found_packets = []
        self.found_handshake = False
    def stop(self):
        self._stop.set()
    def check_packet(self, packet) -> bool:
        self.found_packets.append(packet)
        if packet.haslayer("EAPOL"):
            return True
        return False
    def capture_handshakes(self) -> bool:
        scapy.sniff(filter=f"ether host{globals.selected_bssid}", iface = globals.interface, stop_filter= lambda p: self.check_packet(p) or self._stop.is_set(), timeout = 600)
        if any(p.haslayer("EAPOL") for p in self.found_packets):
            scapy.wrpcap("capture.pcap", self.found_packets)
            self.found_handshake = True

