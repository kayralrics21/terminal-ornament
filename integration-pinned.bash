# KAYRA with pinned header, fallback to responsive prompt if tmux is absent.
[[ $- == *i* ]] && [[ -t 0 && -t 1 ]] && [[ ${TERM:-dumb} != dumb ]] || return 0
[[ -n ${KAYRA_DISABLE:-} ]] && return 0
# Do not nest or repeat the graphical banner inside the session.
[[ -n ${TMUX:-} ]] && return 0
if command -v tmux >/dev/null 2>&1; then
    "$HOME/.local/share/kayra-github-uptime/start-pinned.sh" && exit 0
fi
source "$HOME/.local/share/kayra-github-uptime/integration.bash"
