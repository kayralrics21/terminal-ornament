# KAYRA — GitHub-style uptime for Fedora KDE (v2)

Large green/dark-green contribution squares spell **KAYRA** with **SYSTEM UPTIME**
next to it. Made for Konsole and other Linux terminal emulators.

## Recommended: truly pinned top header

1. On Fedora, install the small terminal multiplexer: `sudo dnf install tmux`
2. Extract the ZIP, open a terminal in the extracted folder, and run `bash install.sh`.
3. **Close and reopen the terminal.**

This version makes a dedicated **fixed top pane**, independent from shell command
output. Its top pane adjusts and redraws as the terminal is resized, while uptime updates live. The
bottom pane is your normal interactive Bash or Zsh shell. Each terminal gets
its own isolated tmux session (your existing tmux sessions are not touched).

This is the **only** provided mode that can keep the banner truly pinned while
command output scrolls and the terminal is repeatedly resized. It works inside
most VT-compatible Linux terminals, provided tmux is installed. Terminal
windows shorter than 13 rows fall back to the prompt mode instead of creating
too-small panes. Tiny pane widths use a compact single-line fallback.

Because it uses tmux, its scrollback behavior and shortcuts follow tmux rules:
`Ctrl+B` then `[` enters scrollback (press `q` to leave); `Ctrl+B` then `d`
detaches. Setting `KAYRA_DISABLE=1` skips the integration when starting a shell.

## Alternative: no tmux dependency

Run `bash install.sh prompt` and reopen the terminal. This version puts the
colored banner **above each interactive Bash/Zsh prompt**, rather than printing
it once to scrollback. The word and uptime automatically adapt to the size of
new prompts; the terminal handles prompt redisplay when its window changes.
It is *not* a sticky overlay: after large command output or during resizing,
you may need to press Enter for a fresh banner. This is a limitation of normal
terminal output, not a redraw bug in the lettering.

If tmux is missing, the default `bash install.sh` automatically falls back to
this mode until tmux becomes available.

## Uninstall

Run `bash uninstall.sh` from the extracted folder and reopen the terminal.

## Other details

- System uptime is obtained from `/proc/uptime`, not the terminal session.
- All colors use standard 256-color ANSI/curses palettes.
- Requires Python 3 (standard on Fedora), no internet or pip modules at runtime.
- The previous version's `.bashrc`/`.zshrc` startup hook is replaced.
- For preview without installation, run `python3 banner.py preview`.
- Other prompt customizations are preserved; pinned mode intentionally does not
  prepend a second banner to the shell running *inside* tmux.
