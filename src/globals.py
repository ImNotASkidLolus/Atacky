import threading

quit_app = False
oui_map = {}

l_bssids = []
l_ssids = []
l_sec = []
l_channels = []
clients = []

interface = "wlan0"
channel = None

selected_ssid = None
selected_bssid = None
selected_client = None
packets = []
gps = None
csv_saver = None
fix = 0
bc = 0
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
larp_mode = False
oui_checker = False
check_ble_devices = False
sniff_packets = False
filter_packets = False
det_gps = False
started_attack = False
handshake_sniff = False

handshake_capture = None
deauth_thread = None
beacon_thread = None
deauth_attack = None
beacon_sp = None
auth_attack = None
auth_thread = None
ble_scan = None
ble_thread = None
sniff_thread = None
handshake_thread = None
sniff = None
sniff_filter = ""
retry_time_left = 10 #time in seconds for retrying the client and wifi network sniffs
scroll_delay = 0.1
times_logged = 0