import threading
l_bssids = []
l_ssids = []
l_sec = []
interface = "wlan0"
channel = None
proc = None
stop_scan = False
lock = threading.Lock()
selected_row = 1
selected_ssid = None
selected_bssid = None