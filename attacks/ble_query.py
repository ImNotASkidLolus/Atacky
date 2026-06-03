import threading
import time
import globals
from scapy.all import sniff
from scapy.layers.bluetooth import (
    BluetoothHCISocket,
    HCI_Hdr,
    HCI_Command_Hdr,
    HCI_Cmd_LE_Set_Scan_Parameters,
    HCI_Cmd_LE_Set_Scan_Enable,
    HCI_LE_Meta_Advertising_Reports,
    HCI_LE_Meta_Advertising_Report,
    EIR_CompleteLocalName,
    EIR_Manufacturer_Specific_Data,
)


class BLEDeviceRecognizer:
    def __init__(self, hci_index=0):
        self._stop_event = threading.Event()
        self._hci_index = hci_index

    def stop(self):
        self._stop_event.set()

    def _enable_scan(self, bt, enable: bool):
        bt.sr(
            HCI_Hdr() /
            HCI_Command_Hdr() /
            HCI_Cmd_LE_Set_Scan_Enable(enable=enable, filter_dups=False)
        )

    def _setup_scan(self, bt):
        # type=0: passive scan (no scan requests sent to advertisers)
        bt.sr(
            HCI_Hdr() /
            HCI_Command_Hdr() /
            HCI_Cmd_LE_Set_Scan_Parameters(type=0)
        )

    def _process_packet(self, pkt):
        if HCI_LE_Meta_Advertising_Reports not in pkt:
            return

        for report in pkt[HCI_LE_Meta_Advertising_Reports].reports:
            device = [str(report.addr)]

            # Walk the EIR data list in the report
            for eir in report.data:
                if EIR_CompleteLocalName in eir:
                    name = eir[EIR_CompleteLocalName].local_name
                    device.append(name.decode(errors="replace"))
                elif EIR_Manufacturer_Specific_Data in eir:
                    msd = bytes(eir[EIR_Manufacturer_Specific_Data].payload)
                    device.append(msd.hex())

            with globals.lock:
                globals.ble_devices.append(device)

    def ble_packet_scan(self):
        bt = BluetoothHCISocket(self._hci_index)

        try:
            self._setup_scan(bt)
            self._enable_scan(bt, enable=True)

            while not self._stop_event.is_set():
                try:
                    sniff(
                        opened_socket=bt,
                        prn=self._process_packet,
                        store=False,
                        timeout=1,
                        lfilter=lambda p: HCI_LE_Meta_Advertising_Reports in p,
                    )
                except Exception as e:
                    time.sleep(1)
        finally:
            try:
                self._enable_scan(bt, enable=False)
            except Exception:
                pass
            bt.close()