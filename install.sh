#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
    echo 'Python 3 is required (Fedora: sudo dnf install python3).' >&2
    exit 1
fi

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
dest="$HOME/.local/share/kayra-github-uptime"
install -d -m 755 -- "$dest"
for file in banner.py live-banner.py start-pinned.sh; do
    install -m 755 -- "$project_dir/$file" "$dest/$file"
done
for file in integration.bash integration.zsh integration-pinned.bash integration-pinned.zsh; do
    install -m 644 -- "$project_dir/$file" "$dest/$file"
done

# Choice: pinned (default) or prompt (no tmux required).
mode="${1:-pinned}"
case "$mode" in
    pinned|prompt) ;;
    *) echo 'usage: bash install.sh [pinned|prompt]' >&2; exit 2 ;;
esac

for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
    [[ -e $rc ]] || touch -- "$rc"
    # Remove both the old and current installers' blocks, keep user config.
    sed -i '/^# >>> KAYRA GITHUB UPTIME >>>$/,/^# <<< KAYRA GITHUB UPTIME <<<$/{d;}' "$rc"
    sed -i '/^\[\[ \$- == \*i\* \]\] && source ~\/\.config\/kayra-banner\.sh && kayra_banner$/d' "$rc"
    case "$rc" in
        *.bashrc) ext='bash' ;;
        *.zshrc) ext='zsh' ;;
    esac
    prefix="integration"
    if [[ $mode == pinned ]]; then prefix="integration-pinned"; fi
    printf '\n# >>> KAYRA GITHUB UPTIME >>>\nsource "$HOME/.local/share/kayra-github-uptime/%s.%s"\n# <<< KAYRA GITHUB UPTIME <<<\n' "$prefix" "$ext" >> "$rc"
done

printf '\nKAYRA installed (%s mode). Close and reopen the terminal.\n' "$mode"
if [[ $mode == pinned ]] && ! command -v tmux >/dev/null 2>&1; then
    printf '\nTo enable the truly fixed, live-updating top header on Fedora:\n'
    printf '  sudo dnf install tmux\n'
    printf 'Until tmux is installed, the prompt-based responsive fallback is used.\n'
fi
