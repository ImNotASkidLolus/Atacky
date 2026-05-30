import curses
import time
import globals
from curses import textpad

def draw_packet_builder(stdscr, box):
    box.attron(curses.color_pair(2))
    box.box()
    box.attroff(curses.color_pair(2))

    box.addstr(1, 1, "Type: ")
    box.addstr(2, 1, "Subtype: ")
    box.addstr(1, 1, "Type: ")
    box.addstr(2, 1, "Subtype: ")
    box.addstr(1, 1, "Type: ")
    box.addstr(2, 1, "Subtype: ")
    
