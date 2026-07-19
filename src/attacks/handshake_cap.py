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
    def check_packet(self, packet):
        if packet.haslayer("Dot11"):
            ad1 = packet.addr1
            ad2 = packet.addr2
            ad3 = packet.addr3
            if ad1 == globals.selected_bssid.lower() or ad2 == globals.selected_bssid.lower() or ad3 == globals.selected_bssid.lower():
                self.found_packets.append(packet)
            if packet.haslayer("EAPOL"):   
                self.eapol_counter += 1

    def capture_handshakes(self):
        scapy.sniff(prn=self.check_packet, iface = globals.interface, stop_filter= lambda p: self.eapol_counter >= 4 or self._stop.is_set())
        if self.eapol_counter >= 4:
            scapy.wrpcap("capture.pcap", self.found_packets)
            self.found_handshake = True

