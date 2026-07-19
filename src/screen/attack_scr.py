import curses
import globals
import attacks.OUI_checker as oui
import time

def draw_attack_screen(attack_box:curses.window, stdscr, width, height):
    attack_box.erase()
    attack_box.attron(curses.color_pair(2))
    attack_box.box()
    attack_box.attroff(curses.color_pair(2))
    attack_box.addstr(1,1, "SELECT YOUR ATTACK TYPE".center(width -2), curses.color_pair(1))
    if globals.selected_row == 1:
        attack_box.addstr(3,1, "1. Deauthentication Attack(DEAUTH)", curses.color_pair(1))
    else:
        attack_box.addstr(3,1, "1. Deauthentication Attack(DEAUTH)", curses.color_pair(4))
    if globals.selected_row == 2:
        attack_box.addstr(4,1, "2. FAKE BEACON FRAME SPAM", curses.color_pair(1))
    else:
        attack_box.addstr(4,1, "2. FAKE BEACON FRAME SPAM", curses.color_pair(4))
    if globals.selected_row == 3:
        attack_box.addstr(5, 1, "3. Authentication flood attack", curses.color_pair(1))
    else:
        attack_box.addstr(5, 1, "3. Authentication flood attack", curses.color_pair(4))
    if globals.selected_row == 4:
        attack_box.addstr(6, 1, "4. Client MAC OUI map lookup", curses.color_pair(1))
    else:
        attack_box.addstr(6, 1, "4. Client MAC OUI map lookup", curses.color_pair(4))
    if globals.selected_row == 5:
        attack_box.addstr(7, 1, "5. Handshake capture", curses.color_pair(1))
    else:
        attack_box.addstr(7, 1, "5. Handshake capture", curses.color_pair(4))
    if globals.clients is None or globals.clients == []:
        attack_box.addstr(8,1, "Clients for this network NOT FOUND!", curses.color_pair(4))
        attack_box.addstr(9, 1, f"Retrying in {globals.retry_time_left}s")
    else:
        attack_box.addstr(8,1, "Clients for this network FOUND!", curses.color_pair(4))        
    attack_box.addstr(height - 2,1, f"SSID: {globals.selected_ssid[:10]} {globals.selected_bssid}".center(width - 2), curses.color_pair(1))

def draw_deauth_screen(attack_box:curses.window, stdscr, width, height):
    attack_box.erase()
    attack_box.attron(curses.color_pair(2))
    attack_box.box()
    attack_box.attroff(curses.color_pair(2))
    if not globals.clients:
        attack_box.addstr(1,1, "No clients found for this network.", curses.color_pair(1))
    else:
        attack_box.addstr(1,1, "DEAUTHENTICATION ATTACK".center(width -2), curses.color_pair(1))
        for i, client in enumerate(globals.clients,start=1):
            try:
                if i < height - 3:
                    if not globals.guided_deauth:
                        attack_box.addstr(i + 1, 1, f"{i}. {client} ->  {oui.check_vendor(client)[:15]}", curses.color_pair(4))
                    if globals.guided_deauth:
                        if globals.selected_client_row == i:
                            attack_box.addstr(i + 1, 1, f"{i}. {client} ->  {oui.check_vendor(client)[:15]}", curses.color_pair(8))
                        else:
                            attack_box.addstr(i + 1, 1, f"{i}. {client} ->  {oui.check_vendor(client)[:15]}", curses.color_pair(4))
                        attack_box.addstr(height - 2, 1, f"GUIDED: {globals.guided_deauth}", curses.color_pair(1))
                        attack_box.addstr(height - 2, 15, f"CLIENT: {globals.selected_client}", curses.color_pair(1))
            except curses.error:
                break
        
def draw_beacon_screen(attack_box, stdscr, width):
    attack_box.erase()
    attack_box.attron(curses.color_pair(2))
    attack_box.box()
    attack_box.attroff(curses.color_pair(2))
    attack_box.addstr(1,1, "BEACON SPAM ATTACK".center(width -2), curses.color_pair(1))
    attack_box.addstr(3,1, f"SSID: {globals.selected_ssid[:10]} {globals.selected_bssid}".center(width -2), curses.color_pair(1))
def draw_auth_screen(attack_box, stdscr, width):
    attack_box.erase()
    attack_box.attron(curses.color_pair(2))
    attack_box.box()
    attack_box.attroff(curses.color_pair(2))
    attack_box.addstr(1,1, "AUTHENTICATION FLOOD ATTACK".center(width - 2), curses.color_pair(1))
    attack_box.addstr(3,1, f"SSID: {globals.selected_ssid[:10]} {globals.selected_bssid}".center(width -2), curses.color_pair(1))
def draw_oui_screen(attack_box, stdscr, width, height):
    attack_box.erase()
    attack_box.attron(curses.color_pair(2))
    attack_box.box()
    attack_box.attroff(curses.color_pair(2))
    attack_box.addstr(1,1, "OUI MAC ADDRESS LOOKUP".center(width -2), curses.color_pair(1))
    if not globals.clients:
        attack_box.addstr(1,1, "No clients found for this network".center(width -2), curses.color_pair(1))
    else:
        for i, client in enumerate(globals.clients,start=1):
            try:
                if i < height - 3:
                    attack_box.addstr(i + 1, 1, f"{i}. {client}  ->  {oui.check_vendor(client)[:15]}", curses.color_pair(4))
            except curses.error:
                break
    attack_box.addstr(height - 2,1, f"SSID: {globals.selected_ssid[:10]} {globals.selected_bssid}".center(width -2), curses.color_pair(1))
def draw_handshake_cap_screen(box, width, height):
    box.erase()
    box.attron(curses.color_pair(2))
    box.box()
    box.attroff(curses.color_pair(2))
    box.addstr(1,1, "HANDSHAKE CAPTURE".center(width -2), curses.color_pair(1))
    if globals.handshake_capture.found_handshake:
        box.addstr(2, 1, "HANDSHAKE FOUND!".center(width -2), curses.color_pair(1))
        time.sleep(3)
        globals.handshake_sniff = False
        if globals.handshake_thread:
            globals.handshake_capture.stop()
            globals.handshake_thread = None
    else:
         box.addstr(2, 1, "HANDSHAKE NOT FOUND!".center(width -2), curses.color_pair(1))
    box.addstr(height - 2,1, f"SSID: {globals.selected_ssid[:10]} {globals.selected_bssid}".center(width -2), curses.color_pair(1))
