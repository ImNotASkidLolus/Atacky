import os
import threading 
import curses
import argparse
import get_networks
import screen.main_tui as main_tui
import screen.attack_scr as attack_scr
import handle_input
import attacks.OUI_checker as oui
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
    curses.init_pair(9, curses.COLOR_GREEN, curses.COLOR_GREEN)

    main_box = curses.newwin(rows - 2, cols - 2, 1, 1)
    attack_box = curses.newwin(12, 50, int((rows - 10)//2)-11, int((cols - 50)//2))
    attack_screen = curses.newwin(15, 50, int((rows-10)//2), int((cols - 50)//2))

    status = curses.newwin(1, cols-1, rows - 3, 1)
    status.attron(curses.color_pair(1))
    status.addstr(0, 2, f" Next update in: {globals.retry_time_left}s".ljust(cols - 7))
    status.addstr(0, cols - 3 - len("Press q or Q to exit "), "Press q or Q to exit")
    status.attroff(curses.color_pair(1))

    stdscr.noutrefresh()
    status.noutrefresh()
    main_box.noutrefresh()
    curses.doupdate()

    while not globals.quit_app:
        
        key = stdscr.getch()

        main_tui.draw_main_box(main_box, stdscr, rows-2, cols-2)
        if globals.attack_menu: 
            attack_scr.draw_attack_screen(attack_box, stdscr)
            if globals.send_deauth:
                attack_scr.draw_deauth_screen(attack_screen, stdscr)
            elif globals.send_beacon:
                attack_scr.draw_beacon_screen(attack_screen, stdscr)
            elif globals.send_auth:
                attack_scr.draw_auth_screen(attack_screen,stdscr)
            elif globals.oui_checker:
                attack_scr.draw_oui_screen(attack_screen, stdscr)

        status.attron(curses.color_pair(1))
        status.addstr(0, 2, f" Next update in: {globals.retry_time_left}s ".ljust(cols - 7))
        status.addstr(0, cols - 3 - len("Press q or Q to exit  "), "Press q or Q to exit ")
        status.attroff(curses.color_pair(1))
        stdscr.noutrefresh()

        main_box.noutrefresh()
        if globals.attack_menu:
            attack_box.noutrefresh()
            if globals.send_deauth or globals.send_beacon or globals.send_auth:
                attack_screen.noutrefresh()
            elif globals.oui_checker:
                attack_screen.noutrefresh()
        status.noutrefresh()

        handle_input.handle_input(key,stdscr)
        curses.doupdate()

#==================argument parser=============================#
argument_parser = argparse.ArgumentParser(description="WIFI SCANNING TOOL")
argument_parser.add_argument("-i", "--interface", type=str, required=True, help="Specify the network interface")
argument_parser.add_argument("-c", "--channel", type=str, help="Specify the channel of scanning")
args = argument_parser.parse_args()
globals.channel = args.channel
globals.interface = args.interface
globals.oui_map = oui.load_oui()
#==================scanner thread init========================#
scanner = get_networks.get_networks()
thread1 = threading.Thread(target=scanner.continuous_running, daemon=True)
thread1.start()
#=====================start main loop=========================#
curses.wrapper(main)
if globals.proc:
    globals.proc.terminate()
if globals.beacon_thread:
    globals.beacon_sp.stop()
if globals.deauth_thread:
    globals.deauth_attack.stop()
scanner.stop()
globals.deauth_thread = None
globals.beacon_sp = None
globals.beacon_thread = None
globals.deauth_attack = None
globals.auth_attack = None
globals.auth_thread = None
print(f"BSSIDS: {globals.l_bssids}\n")
print(f"SSIDS: {globals.l_ssids}\n")
print(f"SECURITY: {globals.l_sec}")
print(f"Clients: {globals.clients}")
print(f"Channels: {globals.l_channels}")
print(f"Selected client: {globals.selected_client}")
if os.path.exists(os.path.expanduser("~/output-01.csv")):
    os.remove(os.path.expanduser("~/output-01.csv"))
