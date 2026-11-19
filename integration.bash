# KAYRA v2 — prompt-based: redraws on shell prompt and on terminal resize.
[[ $- == *i* ]] && [[ -t 1 ]] && [[ ${TERM:-dumb} != dumb ]] || return 0
[[ ${KAYRA_BASH_LOADED:-} == 1 ]] && return 0
KAYRA_BASH_LOADED=1
KAYRA_BANNER_SCRIPT="$HOME/.local/share/kayra-github-uptime/banner.py"
KAYRA_ORIGINAL_PS1=$PS1
KAYRA_LAST_PS1=''

_kayra_set_bash_prompt() {
    local banner
    # Respect unrelated prompt modifications (starship, themes, venv, etc.)
    if [[ ${KAYRA_LAST_PS1:-} != '' && $PS1 != "$KAYRA_LAST_PS1" ]]; then
        KAYRA_ORIGINAL_PS1=$PS1
    fi
    banner="$(python3 "$KAYRA_BANNER_SCRIPT" bash 2>/dev/null)" || return 0
    # Command substitution strips ending newlines. Add one explicitly.
    PS1="${banner}"$'\n'"${KAYRA_ORIGINAL_PS1}"
    KAYRA_LAST_PS1=$PS1
}

# Bash supports PROMPT_COMMAND arrays; preserve all earlier prompt actions.
PROMPT_COMMAND+=( '_kayra_set_bash_prompt' )
