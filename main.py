import os
import threading 
import curses
import argparse
import get_networks
import screen.main_tui as main_tui
import screen.attack_scr as attack_scr
import handle_input
import attacks.OUI_checker as oui
import attacks.ble_query as ble
import screen.draw_ble_menu as ble_menu
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
    ble_window = curses.newwin(rows - 2, cols - 2, 1, 1)

    title = curses.newwin(1, cols - 1, 0, 1)
    title.attron(curses.color_pair(1))
    title.addstr(0, 1, "NETWORK SCANNING AND PENETRATION TESTING TOOL".center(cols - 3))
    title.attroff(curses.color_pair(1))

    input_info = curses.newwin(1, cols - 1, rows - 1, 1)
    input_info.attron(curses.color_pair(1))
    input_info.addstr(0, 1, "S-stop scan G-Guided deauth Up/Down-select options".ljust(cols - 5))
    input_info.attroff(curses.color_pair(1))


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
        elif globals.check_ble_devices:
            ble_menu.draw_main(ble_window)

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
        elif globals.check_ble_devices:
            ble_window.noutrefresh()
        status.noutrefresh()
        input_info.noutrefresh()
        title.noutrefresh()
        handle_input.handle_input(key,stdscr)
        curses.doupdate()

#==================argument parser=============================#
argument_parser = argparse.ArgumentParser(description="WIFI SCANNING TOOL")
argument_parser.add_argument("-i", "--interface", type=str, help="Specify the network interface")
argument_parser.add_argument("-c", "--channel", type=str, help="Specify the channel of scanning")
argument_parser.add_argument("-l", "--larp", action="store_true", help = "Enable LARP mode")
args = argument_parser.parse_args()
globals.channel = args.channel
globals.interface = args.interface
globals.larp_mode = args.larp
if not globals.larp_mode:
    globals.oui_map = oui.load_oui()

#==================scanner thread init========================#
if not globals.larp_mode:
    scanner = get_networks.get_networks()
    thread1 = threading.Thread(target=scanner.continuous_running, daemon=True)
    thread1.start()
else:
    import larp_values
    globals.l_bssids = larp_values.l_bssids
    globals.l_channels = larp_values.l_channels
    globals.l_ssids = larp_values.l_ssids
    globals.l_sec = larp_values.l_sec
    globals.clients = larp_values.l_clients


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
