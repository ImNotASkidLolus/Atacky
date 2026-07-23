import curses
import globals
def draw_main_box(main_box, stdscr, height, width):
        with globals.lock:
            big_data = list(zip(globals.l_ssids, globals.l_bssids, globals.l_sec, globals.l_channels))
            small_data = list(zip(globals.l_ssids, globals.l_channels))
            stop_scan = globals.stop_scan
        main_box.erase()
        main_box.attron(curses.color_pair(2))
        main_box.box()
        main_box.attroff(curses.color_pair(2))   
        row_selected = globals.selected_row
        if globals.attack_menu:
            pass
        else:
            if width > 85:
                main_box.addstr(1, 1, " ".center(width - 2), curses.color_pair(9))
                main_box.addstr(1, 1,  "SSID", curses.color_pair(1))
                main_box.addstr(1, 30, "BSSID", curses.color_pair(1))
                main_box.addstr(1, 53, "SECURITY", curses.color_pair(1))
                main_box.addstr(1, 75, "CHANNEL", curses.color_pair(1))
                for i, (ssid, bssid, sec, ch) in enumerate(big_data, start=1):
                    try:
                        if not stop_scan or row_selected != i + 1:
                            main_box.addstr(i + 1, 1,  ssid[:25], curses.color_pair(4))
                            main_box.addstr(i + 1, 30, bssid, curses.color_pair(4))
                            main_box.addstr(i + 1, 60, sec, curses.color_pair(4))
                            main_box.addstr(i + 1, 75, str(ch), curses.color_pair(4))

                        else:
                            main_box.addstr(i + 1, 1, " ".center(width-2), curses.color_pair(9))
                            main_box.addstr(i + 1, 1,  ssid[:25], curses.color_pair(8))
                            main_box.addstr(i + 1, 30, bssid, curses.color_pair(8))
                            main_box.addstr(i + 1, 60, sec, curses.color_pair(8))
                            main_box.addstr(i + 1, 75, str(ch), curses.color_pair(8))
                    except curses.error:
                        break
                for i in range(height -3):
                    main_box.addstr(i+1, 28, "│", curses.color_pair(2))
                    main_box.addstr(i+1, 52, "│", curses.color_pair(2))
                    main_box.addstr(i+1, 73, "│", curses.color_pair(2))
            else:
                main_box.addstr(1, 1, " ".center(width - 2), curses.color_pair(9))
                main_box.addstr(1, 1, "SSID", curses.color_pair(1))
                main_box.addstr(1, int((5/6) * width) , "CHANNEL", curses.color_pair(1))
                for i, (ssid, ch) in enumerate(small_data, start=1):
                    try:
                        if not stop_scan or row_selected != i + 1:
                            main_box.addstr(i + 1, 1,  ssid[:int((5/6) * width) - 5], curses.color_pair(4))
                            main_box.addstr(i + 1, int((5/6) * width), str(ch), curses.color_pair(4))
                        else:
                            main_box.addstr(i + 1, 1, " ".center(width-2), curses.color_pair(9))
                            main_box.addstr(i + 1, 1,  ssid[:int((5/6) * width) - 5], curses.color_pair(8))
                            main_box.addstr(i + 1, int((5/6) * width), str(ch), curses.color_pair(8))
                    except curses.error:
                        break
                for i in range(height - 3):
                    main_box.addstr(i+1, int((5/6) * width) - 2, "│", curses.color_pair(2))
