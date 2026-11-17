import curses
import globals
def draw_main_box(main_box, stdscr, height, width):
        with globals.lock:
            stop_scan = globals.stop_scan
        main_box.erase()
        main_box.attron(curses.color_pair(2))
        main_box.box()
        main_box.attroff(curses.color_pair(2))   
        row_selected = globals.selected_row
        if globals.attack_menu:
            pass
        else:
            num_of_networks = len(globals.l_bssids)
            loop_count = num_of_networks * 2
            k = 0 # index of the network in the array of networks(globals.l_bssids, globals.l_ssids etc.), it increments by 1 every two loop iterations
            if width > 85:
                main_box.addstr(1, 1, " ".center(width - 2), curses.color_pair(9))
                main_box.addstr(1, 1,  "SSID", curses.color_pair(11))
                main_box.addstr(1, int((3/6) * width)+ 2, "BSSID", curses.color_pair(17))
                main_box.addstr(1, int((3/6) * width) + 20 + 2, "SECURITY", curses.color_pair(15))
                main_box.addstr(1, int((5/6) * width) + 2, "CHANNEL", curses.color_pair(13))
                for i in range(1, loop_count + 2):
                    try:
                        # edge case when the table ends and has to draw different box characters
                        if i == loop_count + 1:
                            for j in range(width):
                                if j == 0:
                                    main_box.addstr(i + 1, j, "├",curses.color_pair(2))
                                elif j == width - 1:
                                    main_box.addstr(i + 1, j, "┤",curses.color_pair(2))
                                elif j == int((3/6) * width) or j == int((3/6) * width) + 20  or j == int((5/6) * width):
                                    main_box.addstr(i + 1, j, "┴", curses.color_pair(2))
                                else:    
                                    main_box.addstr(i + 1, j, "─",curses.color_pair(2))
                            break
                        #every two loop steps draw a table line
                        elif i % 2 != 0:
                            for j in range(width):
                                if j == 0:
                                    main_box.addstr(i + 1, j, "├",curses.color_pair(2))
                                elif j == width - 1:
                                    main_box.addstr(i + 1, j, "┤",curses.color_pair(2))
                                elif j == int((3/6) * width) or j == int((3/6) * width) + 20  or j == int((5/6) * width):
                                    main_box.addstr(i + 1, j, "┼", curses.color_pair(2))
                                else:    
                                    main_box.addstr(i + 1, j, "─",curses.color_pair(2))
                            continue

                        else:
                            main_box.addstr(i+1, int((3/6) * width), "│", curses.color_pair(2))
                            main_box.addstr(i+1, int((3/6) * width) + 20, "│", curses.color_pair(2))
                            main_box.addstr(i+1, int((5/6) * width), "│", curses.color_pair(2))
                        if k < num_of_networks:
                            ssid = globals.l_ssids[k]
                            bssid = globals.l_bssids[k]
                            ch = globals.l_channels[k]
                            sec = globals.l_sec[k]
                            k = k + 1
                        if ch > 13:
                            ssid = f"(5G) {ssid}"
                        if not stop_scan or row_selected != k + 1:
                            main_box.addstr(i + 1, 1,  ssid[:width//2 - 2].replace("\0",""), curses.color_pair(10))
                            main_box.addstr(i + 1, int((3/6) * width) + 2, bssid, curses.color_pair(16))
                            main_box.addstr(i + 1, int((3/6) * width) + 20 + 2, str(sec), curses.color_pair(14))
                            main_box.addstr(i + 1, int((5/6) * width)+ 2, str(ch), curses.color_pair(12))
                        else:
                            main_box.addstr(i + 1, 1, " ".center(width-2), curses.color_pair(9))
                            main_box.addstr(i + 1, 1,  ssid[:width//2 - 2].replace("\0",""), curses.color_pair(11))
                            main_box.addstr(i + 1, int((3/6) * width)+ 2, bssid, curses.color_pair(17))
                            main_box.addstr(i + 1, int((3/6) * width) + 20 + 2,  str(sec), curses.color_pair(15))
                            main_box.addstr(i + 1, int((5/6) * width)+ 2, str(ch), curses.color_pair(13))
                    except curses.error:
                        break  
            # everything below works the same as above, but has less data displayed for better visibility on small screens
            else:
                main_box.addstr(1, 1, " ".center(width - 2), curses.color_pair(9))
                main_box.addstr(1, 1, "SSID", curses.color_pair(11))
                main_box.addstr(1, int((5/6) * width) , "CHANNEL", curses.color_pair(13))
                for i in range(1, loop_count + 2):
                    if i == 1:
                        continue
                    if i == loop_count + 1:
                        for j in range(width):
                            if j == 0:
                                main_box.addstr(i + 1, j, "├",curses.color_pair(2))
                            elif j == width - 1:
                                main_box.addstr(i + 1, j, "┤",curses.color_pair(2))
                            else:    
                                main_box.addstr(i + 1, j, "─",curses.color_pair(2))
                        break
                    elif i % 2 != 0:
                        for j in range(width):
                            if j == 0:
                                main_box.addstr(i + 1, j, "├",curses.color_pair(2))
                            elif j == width - 1:
                                main_box.addstr(i + 1, j, "┤",curses.color_pair(2))
                            else:    
                                main_box.addstr(i + 1, j, "─",curses.color_pair(2))
                        continue
                    else:
                        ssid = globals.l_ssids[k]
                        bssid = globals.l_bssids[k]
                        ch = globals.l_channels[k]
                        sec = globals.l_sec[k]
                        k = k + 1
                    if ch > 13:
                        # every 5GHz network has their channel above 13 so therefore we add this infront of them to distinguish them
                        ssid = f"(5G) {ssid}"
                    try:
                        if not stop_scan or row_selected != k + 1:
                            main_box.addstr(i + 1, 1,  ssid[:int((5/6) * width) - 5].replace("\0",""), curses.color_pair(10))
                            main_box.addstr(i + 1, int((5/6) * width), str(ch), curses.color_pair(12))
                        else:
                            main_box.addstr(i + 1, 1, " ".center(width-2), curses.color_pair(9))
                            main_box.addstr(i + 1, 1,  ssid[:int((5/6) * width) - 5].replace("\0",""), curses.color_pair(11))
                            main_box.addstr(i + 1, int((5/6) * width), str(ch), curses.color_pair(13))
                    except curses.error:
                        break
                for i in range(height - 3):
                    main_box.addstr(i+1, int((5/6) * width) - 2, "│", curses.color_pair(2))
 