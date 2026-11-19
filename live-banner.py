#!/usr/bin/env python3
"""The pinned header, running in its own tmux pane. Requires only stdlib curses."""
import curses
import time

from banner import LARGE, REGULAR, SMALL, uptime

DARK = 235
GREENS = (22, 28, 34, 40, 48)


def main(stdscr):
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    stdscr.nodelay(True)
    stdscr.keypad(True)
    try:
        curses.start_color()
        try:
            curses.use_default_colors()
        except curses.error:
            pass
        if curses.COLORS >= 256:
            for i, color in enumerate((DARK,) + GREENS, start=1):
                curses.init_pair(i, color, color)
            curses.init_pair(7, 246, -1)
            curses.init_pair(8, 48, -1)
        else:
            for i in range(1, 7):
                curses.init_pair(i, curses.COLOR_GREEN if i >= 3 else curses.COLOR_BLACK, curses.COLOR_GREEN if i >= 3 else curses.COLOR_BLACK)
            curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
            curses.init_pair(8, curses.COLOR_GREEN, curses.COLOR_BLACK)
    except curses.error:
        pass

    old_state = None
    while True:
        height, width = stdscr.getmaxyx()
        timer = uptime()
        state = (height, width, timer)
        if state != old_state:
            render(stdscr, height, width, timer)
            old_state = state
        try:
            ch = stdscr.getch()
        except curses.error:
            ch = -1
        if ch == curses.KEY_RESIZE:
            # A resize may arrive before curses returns the new dimensions.
            old_state = None
        time.sleep(0.25)


def render(stdscr, height, width, timer):
    stdscr.erase()
    if height < 1 or width < 2:
        stdscr.noutrefresh()
        curses.doupdate()
        return

    label = 'SYSTEM UPTIME'
    layouts = [
        (LARGE, 2, 2),
        (REGULAR, 2, 2),
        (REGULAR, 1, 1),
        (SMALL, 1, 1),
    ]
    chosen = None
    for font, tile_width, gap in layouts:
        letter_height = len(font['K'])
        name_width = 5 * len(font['K'][0]) * tile_width + 4 * gap
        info_width = max(len(label), len(timer))
        if height >= letter_height and width >= name_width + 2 + info_width + 1:
            chosen = (font, tile_width, gap)
            break

    if chosen is None:
        summary = 'KAYRA  |  ' + timer
        try:
            stdscr.addnstr(0, 0, summary, max(0, width - 1), curses.color_pair(8) | curses.A_BOLD)
        except curses.error:
            pass
    else:
        font, tile_width, gap = chosen
        name_width = 5 * len(font['K'][0]) * tile_width + 4 * gap
        for row in range(len(font['K'])):
            x = 0
            for index, char in enumerate('KAYRA'):
                for col, bit in enumerate(font[char][row]):
                    idx = 2 + ((row * 23 + col * 13 + index * 17) % 4) if bit == '1' else 1
                    try:
                        stdscr.addstr(row, x, ' ' * tile_width, curses.color_pair(idx))
                    except curses.error:
                        pass
                    x += tile_width
                if index != 4:
                    x += gap
        cx = name_width + 2
        middle = len(font['K']) // 2
        try:
            stdscr.addnstr(middle - 1, cx, label, max(0, width - cx - 1), curses.color_pair(7) | curses.A_BOLD)
            stdscr.addnstr(middle + 1, cx, timer, max(0, width - cx - 1), curses.color_pair(8) | curses.A_BOLD)
        except curses.error:
            pass
    stdscr.noutrefresh()
    curses.doupdate()


if __name__ == '__main__':
    curses.wrapper(main)
