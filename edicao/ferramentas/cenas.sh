#!/usr/bin/env bash
# Uso: cenas.sh <video> [limiar=0.3]  -> imprime os tempos (s) das trocas de cena
set -euo pipefail
ffmpeg -v info -i "$1" -vf "select='gt(scene,${2:-0.3})',showinfo" -an -f null - 2>&1 | grep -o 'pts_time:[0-9.]*' | cut -d: -f2
