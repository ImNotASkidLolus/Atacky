import curses
import globals

def draw_attack_screen(attack_box:curses.window, stdscr):
    attack_box.erase()
    attack_box.attron(curses.color_pair(2))
    attack_box.box()
    attack_box.attroff(curses.color_pair(2))
    attack_box.addstr(1,1, "SELECT THE TYPE OF ATTACK YOU WANT TO PERFORM", curses.color_pair(1))
    if globals.selected_row == 1:
        attack_box.addstr(3,1, "1. Deauthentication Attack(DEAUTH)", curses.color_pair(8))
    else:
        attack_box.addstr(3,1, "1. Deauthentication Attack(DEAUTH)", curses.color_pair(3))
    if globals.selected_row == 2:
        attack_box.addstr(4,1, "2. FAKE BEACON FRAME SPAM", curses.color_pair(8))
    else:
        attack_box.addstr(4,1, "2. FAKE BEACON FRAME SPAM", curses.color_pair(3))
    if globals.clients:
        attack_box.addstr(5,1, "Clients for this network FOUND!")
    attack_box.addstr(9,1, f"Selected SSID: {globals.selected_ssid} {globals.selected_bssid}", curses.color_pair(1))

def draw_deauth_screen(attack_box:curses.window, stdscr):
    attack_box.erase()
    attack_box.attron(curses.color_pair(2))
    attack_box.box()
    attack_box.attroff(curses.color_pair(2))
    if globals.clients == None:
        attack_box.addstr(1,1, "No clients found for this network.", curses.color_pair(1))
    else:
        attack_box.addstr(1,1, "DEAUTHENTICATION ATTACK", curses.color_pair(1))
        attack_box.addstr(3,1, f"CLIENTS: {globals.clients}", curses.color_pair(4))
        
def draw_beacon_screen(attack_box, stdscr):
    attack_box.erase()
    attack_box.attron(curses.color_pair(2))
    attack_box.box()
    attack_box.attroff(curses.color_pair(2))
    attack_box.addstr(1,1, "BEACON SPAM ATTACK", curses.color_pair(1))
    attack_box.addstr(3,1, f"Selected SSID: {globals.selected_ssid} {globals.selected_bssid} {globals.channel}", curses.color_pair(1))