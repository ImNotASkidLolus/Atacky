import scapy.all as scapy
import threading
import globals
import time
class Sniffer:
    def __init__(self):
        self._event_key = threading.Event()
    def stop(self):
        self._event_key.set()
    def __dynamic_stop(self):
        return self._event_key.is_set()
    
    def sniff_packets(self):
        scapy.sniff(iface = globals.interface, prn=parse_packet, stop_filter=lambda x: self.__dynamic_stop(), store=0)
    def sniff_packets_filtered(self):
        if globals.packets:
            globals.packets = []
        else:
            scapy.sniff(iface = globals.interface, filter=globals.sniff_filter, prn=parse_packet, stop_filter=lambda x: self.__dynamic_stop(), store=0)
def parse_packet(packet):
    packet = str(packet)
    packet_list = packet.split(' / ')
    packet = ""
    if len(packet_list) > 2:
        packet_list.pop(0)
        packet_list.pop(1)
    for p in packet_list:
        if not "Elt" in p:
            if not "Dot" in p:
                packet += p
                packet += " / "
    time.sleep(globals.scroll_delay)
    globals.packets.append(packet)