import attacks.gps_tracker as gps
l_bssids = [
    "00:1A:2B:3C:4D:5E", "11:22:33:44:55:66", "AA:BB:CC:DD:EE:FF",
    "DE:AD:BE:EF:00:01", "FE:DC:BA:98:76:54", "12:34:56:78:9A:BC",
    "A1:B2:C3:D4:E5:F6", "07:08:09:0A:0B:0C", "FF:EE:DD:CC:BB:AA",
    "10:20:30:40:50:60"
]

l_ssids = [
    "HomeNetwork", "CoffeeShop_WiFi", "Office_5G", "Neighbor_Net",
    "GuestNetwork", "big big big big network name bla bla bla bla bla", "SecureNet_Pro", "HiddenSSID",
    "PublicWiFi", "TestNetwork", "big big big big network name bla bla bla bla bla"
]

l_sec = [
    "WPA2", "WPA3", "WEP", "Open", "WPA2-Enterprise",
    "WPA3", "WPA2", "WPA2-Enterprise", "Open", "WPA3"
]

l_channels = [1, 6, 11, 36, 40, 44, 48, 149, 153, 157]

l_clients = [
    "F0:1D:BC:7E:23:A1", "3C:22:FB:9D:44:12", "88:99:AA:BB:CC:DD",
    "11:AA:33:BB:55:CC", "7E:8F:90:A1:B2:C3", "D4:E5:F6:07:18:29",
    "5A:6B:7C:8D:9E:AF", "C1:D2:E3:F4:05:16", "22:33:44:55:66:77",
    "9F:8E:7D:6C:5B:4A"
]
networks_found = [1,1,11,1,1,11,1,11,12,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
gps = gps.gps_get()
gps.set_larp_values()
