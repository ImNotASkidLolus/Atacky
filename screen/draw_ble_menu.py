import curses
import threading
import time
import globals

def draw_main(box, cols):
    box.addstr(1,1, "BLE DEVICE SCANNING".center(cols - 2), curses.color_pair(1))
    box.attron(curses.color_pair(2))
    box.box()
    box.attroff(curses.color_pair(2))
    try:
        for i, device in enumerate(globals.ble_devices, start=1):
            for j, info in enumerate(device):
                box.addstr(i + 1, j * 10 + 1, f"{info}", curses.color_pair(3))
    except curses.error:
        return
            
