import curses
import globals
def draw_main_box(main_box, stdscr, height, width):
        with globals.lock:
            data = list(zip(globals.l_ssids, globals.l_bssids, globals.l_sec, globals.l_channels))
            stop_scan = globals.stop_scan
        main_box.erase()
        main_box.attron(curses.color_pair(2))
        main_box.box()
        main_box.attroff(curses.color_pair(2))   
        row_selected = globals.selected_row
        if globals.attack_menu:
            pass
        else:
            main_box.addstr(1, 1, " ".center(width - 2), curses.color_pair(9))
            main_box.addstr(1, 1,  "SSID", curses.color_pair(8))
            main_box.addstr(1, 30, "BSSID", curses.color_pair(8))
            main_box.addstr(1, 60, "SECURITY", curses.color_pair(8))
            main_box.addstr(1, 75, "CH", curses.color_pair(8))
            for i, (ssid, bssid, sec, ch) in enumerate(data, start=1):
                try:
                    if not stop_scan or row_selected != i + 1:
                        main_box.addstr(i + 1, 1,  ssid[:20], curses.color_pair(4))
                        main_box.addstr(i + 1, 30, bssid, curses.color_pair(4))
                        main_box.addstr(i + 1, 60, sec, curses.color_pair(4))
                        main_box.addstr(i + 1, 75, ch, curses.color_pair(4))

                    else:
                        main_box.addstr(i + 1, 1, " ".center(width-2), curses.color_pair(9))
                        main_box.addstr(i + 1, 1,  ssid[:20], curses.color_pair(8))
                        main_box.addstr(i + 1, 30, bssid, curses.color_pair(8))
                        main_box.addstr(i + 1, 60, sec, curses.color_pair(8))
                        main_box.addstr(i + 1, 75, ch, curses.color_pair(8))
                except curses.error:
                    break
            for i in range(height -2):
                main_box.addstr(i+1, 28, "│", curses.color_pair(3))
                main_box.addstr(i+1, 52, "│", curses.color_pair(3))
                main_box.addstr(i+1, 73, "│", curses.color_pair(3))

        try:
            main_box.addstr(height - 2, 1,  f"STOP SCAN: {stop_scan}",curses.color_pair(8))
        except curses.error:
            pass
