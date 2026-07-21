import curses
import globals

def draw_gps(main_box):
    try:
        main_box.erase()
        head, bear = "N/A", "N/A"
        if globals.fix and not globals.larp_mode:
            if globals.gps.country_name == "Not found":
                globals.gps.get_country()
            head, bear = globals.gps.get_head_str
        main_box.attron(curses.color_pair(2))
        main_box.box()
        main_box.attroff(curses.color_pair(2))
        
        main_box.addstr(1,5, " Current gps location: ", curses.color_pair(1))
        main_box.addstr(2,2, "Longitude: ", curses.color_pair(3))
        main_box.addstr(2,2 + len("Longitude: "), f"{globals.gps.lon}", curses.color_pair(4))
        main_box.addstr(3,2, "Latitude: ", curses.color_pair(3))
        main_box.addstr(3,2 + len("Latitude: "), f"{globals.gps.lat}", curses.color_pair(4))
        main_box.addstr(4,2, "Altitude:", curses.color_pair(3))
        main_box.addstr(4,2 + len("Altitude: "), f"{globals.gps.alt}m", curses.color_pair(4))
        main_box.addstr(5,2, "Position error(m): ", curses.color_pair(3))
        main_box.addstr(5,2 + len("position error(m): "), f"{globals.gps.get_range_of_position}", curses.color_pair(4))
        main_box.addstr(6,2, "Current country: ", curses.color_pair(3))
        main_box.addstr(6,2 + len("Current country: "), f"{globals.gps.country_name[:15]}", curses.color_pair(4))
        main_box.addstr(7,2, "Current grid square: ", curses.color_pair(3))
        main_box.addstr(7,2+len("current grid square: "), f"{globals.gps.grid_square_position}", curses.color_pair(4))
        main_box.addstr(8,2, "Current speed(m/s): ", curses.color_pair(3))
        main_box.addstr(8,2 + len("Current speed(m/s): "),f"{globals.gps.speed}", curses.color_pair(4))
        main_box.addstr(9,2, "Current speed(km/h): ", curses.color_pair(3))
        main_box.addstr(9,2 + len("Current speed(km/h): "),f"{round(globals.gps.speed * 3.6, 1)}", curses.color_pair(4))
        main_box.addstr(10,2,"Speed error(m/s, km/h): ", curses.color_pair(3))
        if globals.gps.speederr < 50:
            main_box.addstr(10,2 + len("speed error(m/s, km/h): "), f"{round(globals.gps.speederr,1)}, {round(globals.gps.speederr * 3.6,1)}", curses.color_pair(4))
        else:
            main_box.addstr(10,2 + len("speed error(m/s, km/h): "), "Stationary", curses.color_pair(4))
        main_box.addstr(11,2, "Climb rate(m/s): ", curses.color_pair(3))
        main_box.addstr(11,2 + len("Climb rate(m/s): "), f"{globals.gps.climb}", curses.color_pair(4))
        main_box.addstr(12,2, "Heading: ", curses.color_pair(3))
        main_box.addstr(12,2 + len("Heading: "), f"{head}", curses.color_pair(4))
        main_box.addstr(13,2, "Bearing: ", curses.color_pair(3))
        main_box.addstr(13,2 + len("Bearing: "), f"{bear}°T", curses.color_pair(4))
        main_box.addstr(14,2, "Used satellites: ", curses.color_pair(3))
        main_box.addstr(14, 2 + len("used satellites: "), f"{globals.gps.usat}", curses.color_pair(4))
        main_box.addstr(15,2, "Satellites found: ", curses.color_pair(3))
        main_box.addstr(15,2+len("satellites found: "), f"{globals.gps.nsat}", curses.color_pair(4))
    except Exception as e:
        print("Error printing too screen, perhaps your terminal is too small :( main")
        print(e)
def draw_satelite_info(found_satelites_box:curses.window, height):
        found_satelites_box.erase()
        try:
            found_satelites_box.attron(curses.color_pair(2))
            found_satelites_box.box()
            found_satelites_box.attroff(curses.color_pair(2))

            found_satelites_box.addstr(1, 9, " Satelites found: ", curses.color_pair(1))
            i = 2
            if (globals.fix or globals.larp_mode):
                sat = globals.gps.get_satelite_info()
                if globals.gps.nsat == 0:
                    found_satelites_box.addstr(2 , 2, "ID: ", curses.color_pair(3))
                    found_satelites_box.addstr(2, 2+len("ID: "), "N/A  ",curses.color_pair(4))
                    found_satelites_box.addstr(2 , 9 + len("n/a"), "SNR: ", curses.color_pair(3))
                    found_satelites_box.addstr(2, 12 + len("SNR: "), "N/A", curses.color_pair(4))
                    found_satelites_box.addstr(2, 24, "USED: ",curses.color_pair(3))
                    found_satelites_box.addstr(2, 24 + len("USED: "), "N/A", curses.color_pair(4))
                else:
                    for prn, used, snr in sat:
                        found_satelites_box.addstr(i , 2, f"ID: ", curses.color_pair(3))
                        found_satelites_box.addstr(i, 2 + len("ID: "), f"{prn}  ",curses.color_pair(4))
                        found_satelites_box.addstr(i , 12, f"SNR: ", curses.color_pair(3))
                        found_satelites_box.addstr(i, 12 + len("SNR: "), f"{int(snr)}dB  ", curses.color_pair(4))
                        found_satelites_box.addstr(i, 24, f"USED: ",curses.color_pair(3))
                        found_satelites_box.addstr(i, 24 + len("used: "), f"{used}",curses.color_pair(4))
                        if i < height - 2:
                            i = i+1
                        else:
                            i = 2
            else:
                found_satelites_box.addstr(2, 2+len("ID: "), "N/A  ",curses.color_pair(4))
                found_satelites_box.addstr(2 , 9 + len("n/a"), "SNR: ", curses.color_pair(3))
                found_satelites_box.addstr(2, 12 + len("SNR: "), "N/A", curses.color_pair(4))
                found_satelites_box.addstr(2, 24, "USED: ",curses.color_pair(3))
                found_satelites_box.addstr(2, 24 + len("USED: "), "N/A", curses.color_pair(4))
        except Exception:
            print("Error printing too screen, perhaps your terminal is too small :( satellites")
            exit()