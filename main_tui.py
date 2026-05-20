import curses
import globals
def draw_main_box(main_box, stdscr, height, width):
        with globals.lock:
            data = list(zip(globals.l_ssids, globals.l_bssids, globals.l_sec))
            stop_scan = globals.stop_scan
        main_box.erase()
        main_box.attron(curses.color_pair(2))
        main_box.box()
        main_box.attroff(curses.color_pair(2))   
        row_selected = globals.selected_row
        if globals.attack_menu:
            pass
        else:
            for i, (ssid, bssid, sec) in enumerate(data):
                try:
                    if not stop_scan or row_selected != i + 1:
                        main_box.addstr(i + 1, 1,  "SSID: ", curses.color_pair(4))
                        main_box.addstr(i + 1, 7,  ssid[:20], curses.color_pair(3))
                        main_box.addstr(i + 1, 30, "BSSID: ", curses.color_pair(4))
                        main_box.addstr(i + 1, 37, bssid, curses.color_pair(3))
                        main_box.addstr(i + 1, 60, "SECURITY: ", curses.color_pair(4))
                        main_box.addstr(i + 1, 70, sec, curses.color_pair(3))
                    else:
                        main_box.addstr(i + 1, 1,  "SSID: ", curses.color_pair(8))
                        main_box.addstr(i + 1, 7,  ssid[:20], curses.color_pair(8))
                        main_box.addstr(i + 1, 30, "BSSID: ", curses.color_pair(8))
                        main_box.addstr(i + 1, 37, bssid, curses.color_pair(8))
                        main_box.addstr(i + 1, 60, "SECURITY: ", curses.color_pair(8))
                        main_box.addstr(i + 1, 70, sec, curses.color_pair(8))
                except curses.error:
                    break

        try:
            main_box.addstr(height - 2, 1,  f"STOP SCAN: {stop_scan}",curses.color_pair(8))
        except curses.error:
            pass
