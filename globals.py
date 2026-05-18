import threading

l_bssids = []
l_ssids = []
l_sec = []
l_channels = []

interface = "wlan0"
channel = None
clients = None
selected_ssid = None
selected_bssid = None

proc = None
stop_scan = False
lock = threading.Lock()
selected_row = 1
send_deauth = False
attack_menu = False
send_beacon = False
