# KAYRA with pinned header, fallback to responsive prompt if tmux is absent.
[[ -o interactive ]] && [[ -t 0 && -t 1 ]] && [[ ${TERM:-dumb} != dumb ]] || return 0
[[ -n ${KAYRA_DISABLE:-} ]] && return 0
[[ -n ${TMUX:-} ]] && return 0
if (( $+commands[tmux] )); then
    "$HOME/.local/share/kayra-github-uptime/start-pinned.sh" && exit 0
fi
source "$HOME/.local/share/kayra-github-uptime/integration.zsh"
