import curses
import src.globals as globals

def draw_packets(box:curses.window, win_height, win_width, stdscr):
    box.erase()
    box.attron(curses.color_pair(2))
    box.box()
    box.attroff(curses.color_pair(2))
    input_box = curses.newwin(3, 30, 1, 2)
    if globals.filter_packets:
        stdscr.clear()
        curses.noecho()
        input_box.attron(curses.color_pair(2))
        input_box.box()
        input_box.attroff(curses.color_pair(2))
        input_box.addstr(1,1, "Filter: ")
        input_box.refresh()
        input_box.move(1,1)
        curses.echo()
        max_len = 19
        globals.sniff_filter = input_box.getstr(1,10, max_len).decode('utf-8')
        curses.noecho()
        curses.curs_set(0)
        globals.filter_packets = False
    for i, packet_line in enumerate(globals.packets, start= 1):
        if win_height < len(globals.packets):
            globals.packets.pop(0)
        try:
            box.addstr(i, 2, packet_line[:win_width - 3], curses.color_pair(4))
        except curses.error:
            break
