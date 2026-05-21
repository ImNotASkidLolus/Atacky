import csv
import subprocess
import os
import time
import globals
import threading

class get_networks:
    def __init__(self):
        self._event_stop = threading.Event()
    def run_airodump(self, interface, channel=None, bssid=None):
        output_path = os.path.expanduser("~/output")
        command = ["airodump-ng", 
        "--output-format", "csv", 
        "--write", output_path]
        if channel:
            command += ["--channel", str(channel)]
        if bssid:
            command += ["--bssid", str(bssid)]
        command.append(str(interface))

        t_proc = subprocess.Popen(
            command,
            start_new_session=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return t_proc
    def stop(self):
        self._event_stop.set()
    def parse_csv(self, filename):
        channels, bssids, ssids, sec = [], [], [], []
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                # skip header and blank lines, stop at client section
                if not row or row[0].strip() == 'BSSID':
                    continue
                if row[0].strip() == 'Station MAC':
                    break  # client section starts, we only want APs
                if len(row) > 13:
                    bssids.append(row[0].strip())
                    channels.append(row[3].strip())
                    sec.append(row[5].strip())
                    ssids.append(row[13].strip())
        return ssids, bssids, sec, channels
    def parse_clients_csv(self, filename):
        global station_line
        clients = []
        station_line = False
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if not row:
                    continue
                if row[0].strip() == 'Station MAC':
                    station_line = True
                    continue
                if station_line:
                    if len(row) < 6:
                        continue
                    clients.append(row[0].strip())
        return clients
    def continuous_running(self):
        filepath = os.path.expanduser("~/output-01.csv")
        while not self._event_stop.is_set():
            try:
                if not globals.stop_scan:
                    globals.proc = self.run_airodump(globals.interface, globals.channel)
                    waited = 0
                    while not os.path.exists(filepath) and waited < 15:
                        time.sleep(0.5)
                        waited += 0.5
                    time.sleep(10)
                    globals.proc.terminate()
                    globals.proc.wait()
                    ssids, bssids, sec, channels = self.parse_csv(filepath)
                    with globals.lock:
                        globals.l_bssids = bssids
                        globals.l_ssids = ssids
                        globals.l_sec = sec
                        globals.l_channels = channels
                    if os.path.exists(filepath):
                        os.remove(filepath)
                elif globals.attack_menu and not globals.guided_deauth:
                    if globals.proc:
                        globals.proc.terminate()
                        globals.proc.wait()
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    globals.proc = self.run_airodump(globals.interface, channel=globals.channel, bssid=globals.selected_bssid)
                    waited = 0
                    while not os.path.exists(filepath) and waited < 15:
                        time.sleep(0.5)
                        waited += 0.5
                    globals.retry_time_left = 10
                    for _ in range(10):
                        time.sleep(1)
                        globals.retry_time_left -=1
                    globals.proc.terminate()
                    globals.proc.wait()
                    clients = self.parse_clients_csv(filepath)
                    with globals.lock:
                        globals.clients = clients
                    if os.path.exists(filepath):
                        os.remove(filepath)
                else:
                    if globals.proc:
                        globals.proc.terminate()
                        globals.proc.wait()
                    time.sleep(1)
            except Exception as e:
                print(e)
                globals.proc.terminate()
                time.sleep(1)
