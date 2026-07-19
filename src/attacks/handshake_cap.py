import scapy.all as scapy
import globals
import threading
import subprocess
import time

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
    def check_packet(self, p):
    # Since the BPF filter only lets target traffic through, save everything immediately!
        self.found_packets.append(p)
        
        if p.haslayer("EAPOL"):
            # Direction check
            to_ds = p.FCfield & 0b01 != 0 
            if to_ds:
                self.from_frames += 1  # CLI -> AP
                print(f"CLI -> AP (M2/M4) Caught! Total: {self.from_frames}")
            else:
                self.to_frames += 1    # AP -> CLI
                print(f"AP -> CLI (M1/M3) Caught! Total: {self.to_frames}")
            
            # Trigger the buffer window on baseline traffic detection
            if self.to_frames >= 1 and self.from_frames >= 1:
                if not self.found_handshake:
                    print("[+] Handshake activity detected! Keeping 5-second buffer open...")
                    self.found_handshake = True
                    self.start_buffer_time = time.time()

        # Manage the graceful exit window
        if self.found_handshake:
            if time.time() - self.start_buffer_time > 5.0:
                print("[+] Capture window complete. Saving robust PCAP.")
                return True
                
        return False
    def capture_handshakes(self):
        bpf_filter = f"ether proto 0x888e or wlan addr2 {globals.selected_bssid.lower()} or wlan addr3 {globals.selected_bssid.lower()}"
        scapy.sniff(filter = bpf_filter, iface = globals.interface, stop_filter= lambda p: self.check_packet(p) or self._stop.is_set())
        scapy.wrpcapng("capture.pcap", self.found_packets)
        self.found_handshake = True

