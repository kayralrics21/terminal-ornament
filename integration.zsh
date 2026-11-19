# KAYRA v2 — prompt-based: zsh repaints when resized.
[[ -o interactive ]] && [[ -t 1 ]] && [[ ${TERM:-dumb} != dumb ]] || return 0
[[ ${KAYRA_ZSH_LOADED:-} == 1 ]] && return 0
KAYRA_ZSH_LOADED=1
KAYRA_BANNER_SCRIPT="$HOME/.local/share/kayra-github-uptime/banner.py"
KAYRA_ORIGINAL_PROMPT="$PROMPT"
KAYRA_LAST_PROMPT=''

_kayra_set_zsh_prompt() {
    local banner
    if [[ -n "$KAYRA_LAST_PROMPT" && "$PROMPT" != "$KAYRA_LAST_PROMPT" ]]; then
        KAYRA_ORIGINAL_PROMPT="$PROMPT"
    fi
    banner="$(python3 "$KAYRA_BANNER_SCRIPT" zsh 2>/dev/null)" || return 0
    PROMPT="${banner}"$'\n'"${KAYRA_ORIGINAL_PROMPT}"
    KAYRA_LAST_PROMPT="$PROMPT"
}

autoload -Uz add-zsh-hook
add-zsh-hook precmd _kayra_set_zsh_prompt

# Preserve existing TRAPWINCH hooks if the user's theme defines one.
if (( ! $+functions[TRAPWINCH] )); then
    TRAPWINCH() {
        _kayra_set_zsh_prompt
        zle reset-prompt 2>/dev/null || true
    }
fi
