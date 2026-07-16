import os
import src.globals as globals
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def load_oui(path=os.path.join(BASE_DIR, "IEEE_MACS.txt")):
    oui_map = {}
    with open(path, "r") as f:
        for line in f:
            if "(hex)" in line:
                parts = line.split("(hex)")
                mac_prefix = parts[0].strip().replace("-", ":").lower()
                vendor = parts[1].strip()
                oui_map[mac_prefix] = vendor
    return oui_map
def check_vendor(mac):
    mac_prefix = mac[:8].lower()
    vendor = globals.oui_map.get(mac_prefix, "Unknown")
    return vendor