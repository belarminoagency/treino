#!/usr/bin/env bash
# Prepara a sessão para editar: dependências Python (CPU), confere ffmpeg/node/chromium.
# Idempotente: só instala o que falta.
set -euo pipefail
cd "$(dirname "$0")"
VENV="${EDICAO_VENV:-$HOME/.edicao-venv}"
if [ ! -x "$VENV/bin/python" ]; then python3 -m venv "$VENV"; fi
if ! "$VENV/bin/python" -c "import whisperx, cv2, soundfile" 2>/dev/null; then
  "$VENV/bin/pip" install -q --upgrade pip
  "$VENV/bin/pip" install -q -r requirements.txt
fi
command -v ffmpeg >/dev/null || { echo "FALTA ffmpeg"; exit 1; }
command -v node >/dev/null || { echo "FALTA node"; exit 1; }
echo "ok: python=$VENV/bin/python"
