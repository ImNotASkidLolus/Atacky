import csv
import threading
import globals
WIGLE_HEADER = [
    'WigleWifi-1.4',
    'appRelease=Attack-TUI-v0.9',
    'model=custom',
    'release=0.9',
    'device=linux',
    'display=wardrive',
    'board=unknown',
    'brand=unknown',
]

WIGLE_COLS = [
    'MAC','SSID','AuthMode','FirstSeen','Channel',
    'CurrentLatitude','CurrentLongitude','AltitudeMeters','AccuracyMeters','Type'
]
class csv_saver:
    def __init__(self, path):
        self.path = path
        self.seen = set()
        with open(path, 'w', newline='') as f:
            f.write(','.join(WIGLE_HEADER) + '\n')
            w = csv.writer(f)
            w.writerow(WIGLE_COLS)

    def log(self):
        for bssid, essid, channel, privacy in zip(globals.l_bssids, globals.l_ssids, globals.l_channels, globals.l_sec):
            if bssid in self.seen:
                continue
            if globals.gps.lat is 0:
                return
            with globals.lock:
                if bssid in self.seen:
                    continue
                self.seen.add(bssid)
                with open(self.path, 'a', newline='') as f:
                    w = csv.writer(f)
                    w.writerow([
                        bssid,
                        essid,
                        f'[{privacy}]',
                        globals.gps.time,
                        channel,
                        globals.gps.lat,
                        globals.gps.lon,
                        globals.gps.alt,
                        globals.gps.get_range_of_position,
                        'WIFI',
                    ])
                    globals.times_logged+=1
