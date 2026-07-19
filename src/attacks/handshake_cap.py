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
        self.eapol_counter = 0
    def stop(self):
        self._stop.set()
    def check_packet(self, packet) -> bool:
        self.found_packets.append(packet)
        if packet.haslayer("EAPOL"):
            self.eapol_counter += 1

    def capture_handshakes(self):
        scapy.sniff(filter=f"ether host {globals.selected_bssid}", iface = globals.interface, stop_filter= lambda p: self.eapol_counter >= 4 or self._stop.is_set())
        if any(p.haslayer("EAPOL") for p in self.found_packets):
            scapy.wrpcap("capture.pcap", self.found_packets)
            self.found_handshake = True

