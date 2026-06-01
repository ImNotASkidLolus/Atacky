import curses
import threading
import time
import globals

def draw_main(box:curses.win):
    box.addstr(1,1, "Hello ble", curses.color_pair(4))
    box.attron(curses.color_pair(2))
    box.box()
    box.attroff(curses.color_pair(2))
    try:
        for i, device in enumerate(globals.ble_devices, start=1):
            for j, info in enumerate(device):
                box.addstr(i + 1, j * 10 + 1, f"{info}", curses.color_pair(3))
    except curses.error:
        return
            
