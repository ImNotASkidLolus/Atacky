import scapy.all as scapy
import globals
import time
import threading

class ble_device_recognizer:
    def __init__(self):
        self._stop_event = threading.Event()
    def stop(self):
        self._stop_event.set()
    def ble_check_dev(self, pkt):
        if not pkt.haslayer(scapy.BTLE_ADV_IND):
            return
        device = []
        device.append(str(pkt[scapy.BTLE_ADV_IND].AdvA))
        if pkt.haslayer(scapy.EIR_CompleteLocalName):
            device.append(pkt[scapy.EIR_CompleteLocalName].local_name.decode(errors="replace"))

        if pkt.haslayer(scapy.EIR_Manufacturer_Specific_Data):
            device.append(bytes(pkt[scapy.EIR_Manufacturer_Specific_Data].payload).hex())
        with globals.lock:
            globals.ble_devices.append(device)

    def ble_packet_scan(self):
        while not self._stop_event.is_set():
            try:
                scapy.sniff(iface="hci0", prn=self.ble_check_dev, store=False,
                    stop_filter=lambda _: self._stop_event.is_set())
            except Exception as e:
                time.sleep(1)