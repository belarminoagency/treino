#!/usr/bin/env bash
# Uso: folha_contato.sh <video> <saida.jpg> [segundos entre quadros=1] [colunas=8]
# Gera uma folha de contato com o tempo (s) gravado em cada quadro.
set -euo pipefail
v="$1"; out="$2"; step="${3:-1}"; cols="${4:-8}"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
n=$(python3 -c "import math;print(math.ceil($dur/$step))")
rows=$(( (n + cols - 1) / cols ))
ffmpeg -v error -y -i "$v" -vf "fps=1/$step,scale=180:-2,drawtext=text='%{pts\:hms}':x=4:y=4:fontsize=16:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=${cols}x${rows}:padding=2" -frames:v 1 -q:v 4 "$out"
