import threading
import logger.log

log = logger.log()

l_bssids = []
l_ssids = []
l_sec = []
l_channels = []

interface = "wlan0"
channel = None
clients = None
selected_ssid = None
selected_bssid = None
selected_client = None

proc = None
stop_scan = False
lock = threading.Lock()

selected_row = 2
selected_client_row = 1

send_auth = False
send_deauth = False
attack_menu = False
send_beacon = False
guided_deauth = False

retry_time_left = 10 #time in seconds for retrying the client sniff
