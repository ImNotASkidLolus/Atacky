import os
import threading 
import curses
import time
import argparse
import datetime
import deauth
import get_networks
import main_tui
import globals

def main(stdscr):
    rows, cols = stdscr.getmaxyx()
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)
    stdscr.nodelay(True) 
    stdscr.keypad(True)

    #======================COLORS INITIALIZATION=======================#
    curses.init_pair(1, curses.COLOR_BLACK,  curses.COLOR_GREEN) #title bar
    curses.init_pair(2, curses.COLOR_WHITE,  -1) #box border
    curses.init_pair(3, curses.COLOR_GREEN, -1) #label
    curses.init_pair(4, curses.COLOR_MAGENTA,   -1) #value
    curses.init_pair(5, curses.COLOR_RED, -1) #color of the header text
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_WHITE) #color of the KUKI text
    curses.init_pair(7, curses.COLOR_YELLOW, -1) #color of KUKI the cat
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_GREEN)

    main_box = curses.newwin(rows - 10, 80, 1, 1)

    current_time = datetime.datetime.now()                      
    last_time_stamp = current_time.time()
    status = curses.newwin(1, cols-2, rows - 2, 1)
    status.attron(curses.color_pair(1))
    status.addstr(0, 2, f"Last updated: {last_time_stamp}".ljust(cols - 7))
    status.addstr(0, cols - 3 - len("Press q or Q to exit "), "Press q or Q to exit")
    status.attroff(curses.color_pair(1))

    stdscr.noutrefresh()
    status.noutrefresh()
    main_box.noutrefresh()
    curses.doupdate()
    while True:
        current_time = datetime.datetime.now()
        last_time_stamp = current_time.time()
        main_tui.draw_main_box(main_box, stdscr, rows-10, 80)
        status.attron(curses.color_pair(1))
        status.addstr(0, 2, f" Last updated: {last_time_stamp} ".ljust(cols - 7))
        status.addstr(0, cols - 3 - len("Press q or Q to exit  "), "Press q or Q to exit ")
        status.attroff(curses.color_pair(1))
        stdscr.noutrefresh()
        main_box.noutrefresh()
        status.noutrefresh()
        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord('s') or key == ord('S'):
            if not globals.stop_scan:
                if globals.proc:
                    globals.proc.terminate()
                globals.stop_scan = True
            else:
                globals.stop_scan = False
        elif key == curses.KEY_UP:
            with globals.lock:
                if globals.selected_row > 1:
                    globals.selected_row -= 1
        elif key == curses.KEY_DOWN:
            with globals.lock:
                if globals.selected_row <= max(1, len(globals.l_ssids)):
                    globals.selected_row += 1
        elif key in (curses.KEY_ENTER, 10, 13):
            # When scan is stopped, Enter selects the highlighted row
            if globals.stop_scan:
                with globals.lock:
                    idx = globals.selected_row - 1
                    if 0 <= idx < len(globals.l_ssids):
                        globals.selected_ssid = globals.l_ssids[idx]
                        globals.selected_bssid = globals.l_bssids[idx]
        else:
            time.sleep(0.05)
        curses.doupdate()

#==================argument parser=============================#
argument_parser = argparse.ArgumentParser(description="WIFI SCANNING TOOL")
argument_parser.add_argument("-i", "--interface", type=str, required=True, help="Specify the network interface")
argument_parser.add_argument("-c", "--channel", type=str, help="Specify the channel of scanning")
args = argument_parser.parse_args()
globals.channel = args.channel
globals.interface = args.interface
#==================scanner thread init========================#
scanner = get_networks.get_networks()
thread1 = threading.Thread(target=scanner.continuous_running, daemon=True)
thread1.start()

#=====================start main loop=========================#
curses.wrapper(main)
if globals.proc:
    globals.proc.terminate()
print(f"BSSIDS: {globals.l_bssids}\n")
print(f"SSIDS: {globals.l_ssids}\n")
print(f"SECURITY: {globals.l_sec}")
if os.path.exists(os.path.expanduser("~/output-01.csv")):
    os.remove(os.path.expanduser("~/output-01.csv"))

