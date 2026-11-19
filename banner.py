#!/usr/bin/env python3
"""GitHub-like responsive KAYRA prompt; no pip modules required."""
import os
import sys

# Fonts: KAYRA is five individual glyphs, including a repeated A.
LARGE = {
    'K': ('1100011','1100110','1101100','1111000','1111000','1101100','1100110','1100011','1100011'),
    'A': ('0011100','0110110','1100011','1100011','1111111','1100011','1100011','1100011','1100011'),
    'Y': ('1100011','1100011','0110110','0011100','0001000','0001000','0001000','0001000','0001000'),
    'R': ('1111100','1100110','1100011','1111100','1110000','1101100','1100110','1100011','1100011'),
}
REGULAR = {
    'K': ('10001','10010','10100','11000','10100','10010','10001'),
    'A': ('01110','10001','10001','11111','10001','10001','10001'),
    'Y': ('10001','01010','00100','00100','00100','00100','00100'),
    'R': ('11110','10001','10001','11110','10100','10010','10001'),
}
SMALL = {
    'K': ('101','110','110','101','101'),
    'A': ('010','101','111','101','101'),
    'Y': ('101','101','010','010','010'),
    'R': ('110','101','110','101','101'),
}

# GitHub dark contributions colors, nearest widely-supported 256-color equivalents.
COLORS = ('22', '28', '34', '40', '48')
INACTIVE = '235'
SOFT_TEXT = '245'
BRIGHT_TEXT = '48'
RESET = '\x1b[0m'


def size():
    # stdout is a pipe for bash/zsh prompt command substitution, so inspect tty.
    for fd in (2, 0, 1):
        try:
            dim = os.get_terminal_size(fd)
            return max(1, dim.columns), max(1, dim.lines)
        except OSError:
            pass
    try:
        with open('/dev/tty', 'rb') as tty:
            dim = os.get_terminal_size(tty.fileno())
        return max(1, dim.columns), max(1, dim.lines)
    except OSError:
        return int(os.environ.get('COLUMNS', '80') or '80'), int(os.environ.get('LINES', '24') or '24')


def uptime():
    try:
        with open('/proc/uptime', encoding='ascii') as handle:
            seconds = int(float(handle.read().split()[0]))
    except (OSError, ValueError, IndexError):
        return 'unknown'
    d, remainder = divmod(seconds, 86400)
    h, remainder = divmod(remainder, 3600)
    m, s = divmod(remainder, 60)
    if d:
        return f'{d}d {h:02}h {m:02}m'
    if h:
        return f'{h}h {m:02}m {s:02}s'
    return f'{m}m {s:02}s'


def wrap(s, prompt_type):
    if prompt_type == 'bash':
        return '\\[' + s + '\\]'
    if prompt_type == 'zsh':
        return '%{' + s + '%}'
    return s


def style(text, color, prompt_type, *, bg=False, bold=False):
    sel = f'{"48" if bg else "38"};5;{color}'
    if bold:
        sel = '1;' + sel
    return wrap('\x1b[' + sel + 'm', prompt_type) + text + wrap(RESET, prompt_type)


def render(prompt_type):
    cols, rows = size()
    # Leave one spare column to prevent autowrap on Konsole, GNOME Terminal,
    # xterm, Alacritty, kitty and similar VT-compatible terminal emulators.
    usable = max(1, cols - 1)
    timer = uptime()
    label = 'SYSTEM UPTIME'
    info_width = max(len(timer), len(label))

    # The terminal might be short as well as narrow.
    modes = [
        (LARGE, 2, 2, 9, 2),
        (REGULAR, 2, 2, 7, 2),
        (REGULAR, 1, 1, 7, 2),
        (SMALL, 1, 1, 5, 2),
    ]
    chosen = None
    for font, tile_width, gap_width, height, side_gap in modes:
        glyph_width = len(font['K'][0])
        name_width = 5 * glyph_width * tile_width + 4 * gap_width
        entire_width = name_width + side_gap + info_width
        # Extra lines leave space for the user's ordinary prompt and commands.
        if entire_width <= usable and height + 3 <= rows:
            chosen = (font, tile_width, gap_width, height, side_gap)
            break

    if chosen is None:
        # Extremely small terminals still get a usable prompt, no giant banner.
        text = 'KAYRA  ' + timer
        if len(text) > usable:
            text = 'KAYRA ' + timer
        if len(text) > usable:
            text = 'KAYRA' if usable >= 5 else 'K'[:usable]
        return style(text, BRIGHT_TEXT, prompt_type, bold=True) + '\n' if cols >= 2 and rows >= 3 else ''

    font, tile_width, gap_width, height, side_gap = chosen
    out = []
    # Keep the top line flush with the window top when possible.
    for r in range(height):
        line = []
        for l, char in enumerate('KAYRA'):
            for c, bit in enumerate(font[char][r]):
                # Five-level GitHub contribution-style intensity per square.
                color = COLORS[1 + ((r * 23 + c * 13 + l * 17) % 4)] if bit == '1' else INACTIVE
                line.append(style(' ' * tile_width, color, prompt_type, bg=True))
            if l < 4:
                line.append(' ' * gap_width)
        line.append(' ' * side_gap)
        middle = height // 2
        if r == middle - 1:
            line.append(style(label, SOFT_TEXT, prompt_type, bold=True))
        elif r == middle + 1:
            line.append(style(timer, BRIGHT_TEXT, prompt_type, bold=True))
        out.append(''.join(line))

    # Blank line separates the banner and the existing original shell prompt.
    return '\n'.join(out) + '\n\n'


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'preview'
    if mode not in ('bash', 'zsh', 'preview'):
        raise SystemExit('usage: banner.py [bash|zsh|preview]')
    sys.stdout.write(render(mode))


if __name__ == '__main__':
    main()
