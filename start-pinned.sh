#!/usr/bin/env bash
# Launch a separate, per-terminal tmux session with a permanent top header.
set -u
[[ -z ${TMUX:-} ]] || exit 1
command -v tmux >/dev/null 2>&1 || exit 1

root="$HOME/.local/share/kayra-github-uptime"
[[ -r "$root/live-banner.py" ]] || exit 1
# A unique socket prevents interaction with a user's other tmux sessions.
socket="kayra-$BASHPID"
server=(tmux -L "$socket")
rows=24 cols=80
if read -r rows cols < <(stty size </dev/tty 2>/dev/null); then :; fi
[[ $rows =~ ^[0-9]+$ ]] || rows=24
[[ $cols =~ ^[0-9]+$ ]] || cols=80
# Fall back to the prompt mode in tiny windows instead of creating unusable panes.
((rows >= 13 && cols >= 20)) || exit 1
header_height=11
((rows < 17)) && header_height=7

"${server[@]}" -f /dev/null new-session -d -s kayra -x "$cols" -y "$rows" -c "$PWD" || exit 1
"${server[@]}" set-option -g status off
"${server[@]}" set-option -g default-terminal screen-256color
"${server[@]}" set-option -g pane-border-style fg=colour235
bottom=$("${server[@]}" display-message -p -t kayra '#{pane_id}') || exit 1
if ! "${server[@]}" split-window -d -v -b -l "$header_height" -t "$bottom" -- python3 "$root/live-banner.py"; then
    "${server[@]}" kill-session -t kayra >/dev/null 2>&1 || true
    exit 1
fi
# Exit the session when either the user's shell or the banner pane exits.
"${server[@]}" set-hook -g pane-exited 'kill-session -t kayra'
"${server[@]}" set-hook -g client-detached 'kill-session -t kayra'
"${server[@]}" select-pane -t "$bottom"
"${server[@]}" -2 attach-session -t kayra
