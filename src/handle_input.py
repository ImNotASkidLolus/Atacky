from attacks import authattack, beacon_spam, deauth as deauth
import globals
import threading
import curses
if not globals.larp_mode:
    from attacks import (
        sniffer as sniffer
    )
import time
import signal 
import sys

sigflag = 0

def catch_int(sig_num, frame):
    global sigflag
    sigflag = 1
def handle_input(key, stdscr):
    signal.signal(signal.SIGINT, catch_int)
    if key == ord('q') or key == ord('Q'):
        globals.quit_app = True
    elif sigflag:
        globals.quit_app = True
    elif key == ord('s') or key == ord('S'):
        if not globals.stop_scan:
            if globals.proc:
                globals.proc.terminate()
            globals.stop_scan = True
        elif globals.selected_bssid and globals.selected_ssid:
            pass
        else:
            globals.stop_scan = False
    elif key == ord('p') or key == ord('P'):
        if not globals.larp_mode:
            if not globals.sniff_packets:
                globals.stop_scan = False
                globals.sniff_packets = True
                globals.packets = []
                globals.sniff = sniffer.Sniffer()
                globals.sniff_thread = threading.Thread(target=globals.sniff.sniff_packets, daemon=True)
                globals.sniff_thread.start()
            else:
                globals.stop_scan = True
                globals.sniff_packets = False
                globals.sniff.stop()
                globals.sniff = None
                globals.sniff_thread = None
                globals.packets = []
    elif key == ord('f') or key == ord('F'):
        if globals.sniff_packets:
            if not globals.filter_packets:
                globals.filter_packets = True
                globals.sniff.stop()
                globals.sniff = sniffer.Sniffer()
                globals.sniff_thread = None
                globals.sniff_thread = threading.Thread(target=globals.sniff.sniff_packets_filtered, daemon=True)
                globals.sniff_thread.start()
            else:
                globals.filter_packets = False
                globals.sniff.stop()
                globals.sniff = None
                globals.sniff_thread = None
                globals.packets = []
    elif key == ord('r') or key == ord('R'):
        if globals.sniff_packets:
            globals.filter_packets = False
            globals.sniff_filter = ""
            globals.packets = []
            globals.sniff.stop()
            globals.sniff = sniffer.Sniffer()
            globals.sniff_thread = threading.Thread(target=globals.sniff.sniff_packets, daemon=True)
            globals.sniff_thread.start()


    elif key == ord('g') or key == ord('G'):
        if globals.send_deauth:
            if not globals.guided_deauth:
                globals.guided_deauth = True
                globals.selected_client_row = 1
                if globals.deauth_attack:
                    globals.deauth_attack.stop()
                globals.deauth_thread = None
                globals.deauth_attack = None
            else:
                globals.guided_deauth = False
                globals.selected_client = None
                globals.selected_client_row = 1
                if globals.deauth_attack:
                    globals.deauth_attack.stop()
                globals.deauth_thread = None
                globals.deauth_attack = None
    elif key == ord('t') or key == ord('T'):
        if not globals.det_gps:
            globals.det_gps = True
        else:
            globals.det_gps = False
    elif key == curses.KEY_UP:
        with globals.lock:
            if globals.attack_menu and not globals.guided_deauth:
                if globals.selected_row > 1:
                    globals.selected_row -= 1
            if globals.guided_deauth and not globals.selected_client:
                if globals.selected_client_row > 1:
                    globals.selected_client_row -= 1
        if globals.selected_row > 1 and not globals.attack_menu:
            globals.selected_row -= 1
        if globals.sniff_packets:
            if globals.scroll_delay < 1:
                globals.scroll_delay += 0.1
    elif key == curses.KEY_DOWN:
        with globals.lock:
            if globals.attack_menu and not globals.guided_deauth:
                if globals.selected_row < 4:
                    globals.selected_row += 1
            if globals.guided_deauth and not globals.selected_client:
                if globals.selected_client_row < max(1, len(globals.clients)):
                    globals.selected_client_row += 1
        if globals.selected_row <= max(1, len(globals.l_ssids)) and not globals.attack_menu:
            globals.selected_row += 1
        if globals.sniff_packets:
            if globals.scroll_delay > 0:
                globals.scroll_delay -= 0.1
            elif globals.scroll_delay < 0:
                globals.scroll_delay = 0

    elif key == curses.KEY_BACKSPACE or key == curses.KEY_LEFT:
        if globals.send_deauth:
            globals.send_deauth = False
            globals.guided_deauth = False
            if globals.deauth_attack is not None:
                globals.deauth_attack.stop()
                globals.deauth_thread = None
                globals.deauth_attack = None
            stdscr.clear()
        elif globals.send_beacon:
            globals.send_beacon = False
            if globals.beacon_sp is not None:
                globals.beacon_sp.stop()
                globals.beacon_thread = None
                globals.beacon_sp = None
                
            stdscr.clear()
        elif globals.send_auth:
            globals.send_auth = False
            if globals.auth_attack is not None:
                globals.auth_attack.stop()
                globals.auth_thread = None
                globals.auth_attack = None
            stdscr.clear()
        elif globals.oui_checker:
            globals.oui_checker = False
        elif globals.attack_menu:
            globals.attack_menu = False
            globals.selected_ssid = None
            globals.selected_bssid = None
            globals.clients = ""
            globals.selected_row = 2
            if globals.proc:
                globals.proc.terminate()
            stdscr.clear()
        elif globals.sniff_packets:
            globals.sniff_packets = False
            globals.sniff.stop()
            globals.sniff_thread = None
        elif globals.det_gps:
            globals.det_gps = False
        stdscr.clear()
        
    elif key in (curses.KEY_ENTER, 10, 13):
        if globals.stop_scan and not globals.attack_menu:
            with globals.lock:
                idx = globals.selected_row - 2
                if 0 <= idx < len(globals.l_ssids):
                    globals.selected_ssid = globals.l_ssids[idx]
                    globals.selected_bssid = globals.l_bssids[idx]
                    if globals.l_channels[idx]:
                        globals.channel = globals.l_channels[idx]
                    globals.selected_row = 1
                    globals.retry_time_left = 10
                    globals.attack_menu = True
        elif globals.attack_menu and not globals.guided_deauth:
            if globals.selected_row == 1 and not globals.send_auth and not globals.send_beacon:
                if globals.clients and (globals.deauth_thread is None or not globals.deauth_thread.is_alive()):
                    if not globals.guided_deauth:
                        globals.send_deauth = True
                        globals.deauth_attack = deauth.DeauthAttack()
                        globals.deauth_thread = threading.Thread(target=globals.deauth_attack.start_deauth, daemon=True)
                        globals.deauth_thread.start()
                else:
                    pass
            elif globals.selected_row == 2 and not globals.send_auth and not globals.send_deauth:
                if not globals.send_beacon and (globals.beacon_thread is None or not globals.beacon_thread.is_alive()):
                    globals.send_beacon = True
                    globals.beacon_sp = beacon_spam.BeaconSpam()
                    globals.beacon_thread = threading.Thread(target=globals.beacon_sp.start_beacon_spam, daemon=True)
                    globals.beacon_thread.start()
                    globals.proc.terminate()
                else:
                    pass
            elif globals.selected_row == 3 and not globals.send_beacon and not globals.send_deauth:
                if not globals.send_auth and (globals.auth_thread is None or not globals.auth_thread.is_alive()):
                    globals.send_auth = True
                    globals.auth_attack = authattack.auth_attack()
                    globals.auth_thread = threading.Thread(target=globals.auth_attack.start_auth_attack, daemon=True)
                    globals.auth_thread.start()
            elif globals.selected_row == 4 and not globals.send_deauth and not globals.send_auth and not globals.send_beacon:
                if not globals.oui_checker:
                    globals.oui_checker = True
        elif globals.guided_deauth and globals.send_deauth:
            for i in range(min(10, len(globals.clients))):
                if i + 1 == globals.selected_client_row:
                    globals.selected_client = globals.clients[i]
                    globals.send_deauth = True
                    globals.deauth_attack = deauth.DeauthAttack()
                    globals.deauth_thread = threading.Thread(target=globals.deauth_attack.start_deauth, daemon=True)
                    globals.deauth_thread.start()

    else:
        time.sleep(0.05)