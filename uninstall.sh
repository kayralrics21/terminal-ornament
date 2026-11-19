#!/usr/bin/env bash
set -euo pipefail
for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [[ -f $rc ]]; then
        sed -i '/^# >>> KAYRA GITHUB UPTIME >>>$/,/^# <<< KAYRA GITHUB UPTIME <<<$/{d;}' "$rc"
        sed -i '/^\[\[ \$- == \*i\* \]\] && source ~\/\.config\/kayra-banner\.sh && kayra_banner$/d' "$rc"
    fi
done
for file in banner.py live-banner.py start-pinned.sh integration.bash integration.zsh integration-pinned.bash integration-pinned.zsh banner.sh; do
    rm -f -- "$HOME/.local/share/kayra-github-uptime/$file"
done
rmdir -- "$HOME/.local/share/kayra-github-uptime" 2>/dev/null || true
printf 'KAYRA removed. Close and reopen the terminal.\n'
