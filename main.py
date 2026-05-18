import os
import threading 
import curses
import time
import argparse
import datetime
import attacks.deauth as deauth
import get_networks
import main_tui
import attacks.attack_scr as attack_scr
import attacks.beacon_spam
import globals

deauth_thread = None
beacon_thread = None
deauth_attack = None
beacon_sp = None

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

    main_box = curses.newwin(rows - 2, cols - 2, 1, 1)
    attack_box = curses.newwin(10, 50, int((rows - 10)//2)-11, int((cols - 50)//2))
    attack_screen = curses.newwin(10, 50, int((rows-10)//2), int((cols - 50)//2))

    current_time = datetime.datetime.now()                      
    last_time_stamp = current_time.time()
    status = curses.newwin(1, cols-1, rows - 2, 1)
    status.attron(curses.color_pair(1))
    status.addstr(0, 2, f"Last updated: {last_time_stamp}".ljust(cols - 7))
    status.addstr(0, cols - 3 - len("Press q or Q to exit "), "Press q or Q to exit")
    status.attroff(curses.color_pair(1))

    stdscr.noutrefresh()
    status.noutrefresh()
    main_box.noutrefresh()
    curses.doupdate()

    while True:
        global deauth_thread, deauth_attack, beacon_sp, beacon_thread
        current_time = datetime.datetime.now()
        last_time_stamp = current_time.time()

        main_tui.draw_main_box(main_box, stdscr, rows-2, cols-2)

        key = stdscr.getch()

        if globals.stop_scan and globals.selected_ssid and globals.selected_bssid: 
            attacks.attack_scr.draw_attack_screen(attack_box, stdscr)
            if globals.send_deauth:
                attacks.attack_scr.draw_deauth_screen(attack_screen, stdscr)
            elif globals.send_beacon:
                attacks.attack_scr.draw_beacon_screen(attack_screen, stdscr)

        status.attron(curses.color_pair(1))
        status.addstr(0, 2, f" Last updated: {last_time_stamp} ".ljust(cols - 7))
        status.addstr(0, cols - 3 - len("Press q or Q to exit  "), "Press q or Q to exit ")
        status.attroff(curses.color_pair(1))
        stdscr.noutrefresh()

        if globals.attack_menu:
            attack_box.noutrefresh()
            if globals.send_deauth or globals.send_beacon:
                attack_screen.noutrefresh()
        else:
            main_box.noutrefresh()
        status.noutrefresh()

        if key == ord('q') or key == ord('Q'):
            break

        elif key == ord('s') or key == ord('S'):
            if not globals.stop_scan:
                if globals.proc:
                    globals.proc.terminate()
                globals.stop_scan = True
            elif globals.selected_bssid and globals.selected_ssid:
                pass
            else:
                globals.stop_scan = False

        elif key == curses.KEY_UP:
            with globals.lock:
                if globals.selected_row > 1 and not globals.attack_menu:
                    globals.selected_row -= 1
                elif globals.attack_menu:
                    if globals.selected_row > 1:
                        globals.selected_row -= 1

        elif key == curses.KEY_DOWN:
            with globals.lock:
                if globals.selected_row <= max(1, len(globals.l_ssids)) and not globals.attack_menu:
                    globals.selected_row += 1
                elif globals.attack_menu:
                    if globals.selected_row < 2:
                        globals.selected_row += 1

        elif key == curses.KEY_BACKSPACE:
            if globals.send_deauth:
                globals.send_deauth = False
                if deauth_attack is not None:
                    deauth_attack.stop()
                    deauth_thread = None
                    deauth_attack = None
                stdscr.refresh()
            elif globals.send_beacon:
                globals.send_beacon = False
                if beacon_sp is not None:
                    beacon_sp.stop()
                    beacon_thread = None
                    beacon_sp = None
            elif globals.attack_menu:
                globals.attack_menu = False
                globals.selected_ssid = None
                globals.selected_bssid = None
                globals.clients = None
                if globals.proc:
                        globals.proc.terminate()
                stdscr.refresh()
            
        elif key in (curses.KEY_ENTER, 10, 13):
            if globals.stop_scan and not globals.attack_menu:
                with globals.lock:
                    idx = globals.selected_row - 1
                    if 0 <= idx < len(globals.l_ssids):
                        globals.selected_ssid = globals.l_ssids[idx]
                        globals.selected_bssid = globals.l_bssids[idx]
                        if globals.l_channels[idx]:
                            globals.channel = globals.l_channels[idx]
                        globals.selected_row = 1
                        globals.attack_menu = True
            elif globals.attack_menu and not globals.send_deauth:
                if globals.selected_row == 1:
                    if globals.clients and (deauth_thread is None or not deauth_thread.is_alive()):
                        globals.send_deauth = True
                        deauth_attack = deauth.DeauthAttack()
                        deauth_thread = threading.Thread(target=deauth_attack.start_deauth, daemon=True)
                        deauth_thread.start()
                    else:
                        pass
                elif globals.selected_row == 2:
                    if not globals.send_beacon and (beacon_thread is None or not beacon_thread.is_alive()):
                        globals.send_beacon = True
                        beacon_sp = attacks.beacon_spam.BeaconSpam()
                        beacon_thread = threading.Thread(target=beacon_sp.start_beacon_spam, daemon=True)
                        beacon_thread.start()
                    else:
                        pass


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
print(f"Clients: {globals.clients}")
print(f"Channels: {globals.l_channels}")
if os.path.exists(os.path.expanduser("~/output-01.csv")):
    os.remove(os.path.expanduser("~/output-01.csv"))
