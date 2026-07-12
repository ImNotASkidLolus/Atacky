import os
import threading 
import curses
import argparse
import get_networks
import screen.main_tui as main_tui
import screen.attack_scr as attack_scr
import screen.sniffer_scr as sniff_scr
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
    curses.init_pair(1, curses.COLOR_BLACK,  curses.COLOR_GREEN)  # title bar and label text — keeping classic phosphor green bg
    curses.init_pair(2, curses.COLOR_CYAN,   -1)                  # box border color — #8BE9FD dracula cyan
    curses.init_pair(4, curses.COLOR_MAGENTA, -1)                 # values text — curses MAGENTA maps close to #BD93F9 dracula purple
    curses.init_pair(6, curses.COLOR_BLACK,  curses.COLOR_CYAN)   # was yellow/white — now black on cyan, clean and readable
    curses.init_pair(8, curses.COLOR_BLACK,  curses.COLOR_GREEN)  # line select text — unchanged, this one was already correct
    curses.init_pair(9, curses.COLOR_GREEN,  curses.COLOR_GREEN)  # green bar — unchanged, solid fill needs to stay green
    
    main_box = curses.newwin(rows - 3, cols - 2, 1, 1)
    attack_box = curses.newwin(12, 50, int((rows - 10)//2)-11, int((cols - 50)//2))
    attack_screen = curses.newwin(15, 50, int((rows-10)//2), int((cols - 50)//2))
    status = curses.newwin(1, cols-1, rows - 3, 1)
    title = curses.newwin(1, cols - 1, 0, 1)
    input_info = curses.newwin(1, cols - 1, rows - 1, 1)
    def draw_title():
        title.attron(curses.color_pair(1))
        title.addstr(0, 1, "NETWORK SCANNING AND PENETRATION TESTING TOOL".center(cols - 3))
        title.attroff(curses.color_pair(1))
    def draw_input_info():
        input_info.attron(curses.color_pair(1))
        input_info.addstr(0, 1, "P-Packet sniff S-stop scan G-Guided deauth Up/Down-select options".ljust(cols - 5))
        input_info.attroff(curses.color_pair(1))
    def draw_status():
        status.attron(curses.color_pair(1))
        status.addstr(0, 2, f" Next update in: {globals.retry_time_left}s".ljust(cols - 7))
        status.addstr(0, cols - 3 - len("Press q or Q to exit "), "Press q or Q to exit")
        status.attroff(curses.color_pair(1))

    stdscr.noutrefresh()
    status.noutrefresh()
    input_info.noutrefresh()
    title.noutrefresh()
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
        elif globals.sniff_packets:
            sniff_scr.draw_packets(main_box, rows - 3, cols - 2, stdscr)
        draw_input_info()
        draw_status()
        draw_title()

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
        input_info.noutrefresh()
        title.noutrefresh()
        handle_input.handle_input(key,stdscr)
        curses.doupdate()

#==================argument parser=============================#
argument_parser = argparse.ArgumentParser(description="WIFI AND BLE SCANNING TOOL")
argument_parser.add_argument("-i", "--interface", type=str, help="Specify the network interface")
argument_parser.add_argument("-c", "--channel", type=str, help="Specify the channel of scanning")
argument_parser.add_argument("-l", "--larp", action="store_true", help = "Enable LARP mode")
args = argument_parser.parse_args()
globals.channel = args.channel
globals.interface = args.interface
globals.larp_mode = args.larp
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
if globals.auth_thread:
    globals.auth_attack.stop()
if globals.sniff_thread:
    globals.sniff.stop()
scanner.stop()
print(f"BSSIDS: {globals.l_bssids}\n")
print(f"SSIDS: {globals.l_ssids}\n")
print(f"SECURITY: {globals.l_sec}")
print(f"Clients: {globals.clients}")
print(f"Channels: {globals.l_channels}")
print(f"Selected client: {globals.selected_client}")
if os.path.exists(os.path.expanduser("~/output-01.csv")):
    os.remove(os.path.expanduser("~/output-01.csv"))
