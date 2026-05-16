import csv
import subprocess
import os
import time
import globals

class get_networks:
    def run_airodump(self, interface, channel=None):
        output_path = os.path.expanduser("~/output")
        command = ["airodump-ng", 
        "--output-format", "csv", 
        "--write", output_path]
        if channel:
            command += ["--channel", str(channel)]
        command.append(str(interface))
        t_proc = subprocess.Popen(
            command,
            start_new_session=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return t_proc
    def parse_csv(self, filename):
        bssids, ssids, sec = [], [], []
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
                    sec.append(row[5].strip())
                    ssids.append(row[13].strip())
        return ssids, bssids, sec

    def continuous_running(self):
        while True:
            try:
                if not globals.stop_scan:
                    globals.proc = self.run_airodump(globals.interface, globals.channel)
                    filepath = os.path.expanduser("~/output-01.csv")
                    waited = 0
                    while not os.path.exists(filepath) and waited < 15:
                        time.sleep(0.5)
                        waited += 0.5
                    time.sleep(10)
                    globals.proc.terminate()
                    globals.proc.wait()
                    ssids, bssids, sec = self.parse_csv(filepath)
                    with globals.lock:
                        globals.l_bssids = bssids
                        globals.l_ssids = ssids
                        globals.l_sec = sec
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
