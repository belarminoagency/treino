---
name: edit-final
description: "Junta tudo (cortes, câmera, animações, legendas e sons), acerta o volume para o padrão do Reels/TikTok e entrega o vídeo pronto para baixar no celular. Use em /edit-final, após a edit-sfx."
---

# edit-final

Monta o vídeo final com FFmpeg e entrega. É a revisão final com vídeo combinada com a pessoa.

- **Lê:** `cortes`, `camera/keyframes.json`, `motions.itens[].render`, `legendas` (render), `sfx`, perfil `estilo-som.md`; `fluxo-de-edicao/guias/entrega-no-editor.md` (caminho C).
- **Escreve:** `Renders/<projeto>_final_vNN.mp4` (fora do git), bloco `final` (versão, duração, loudness).
- **Fim do fluxo.**

Se a `sfx` não estiver `concluido`, pare e sugira terminá-la. Brutos e renders ausentes (sessão nova): refazer pelos scripts a partir do estado; brutos, pedir à pessoa.

## Montagem (ordem das camadas)
1. Segmentos do corte no vídeo de trabalho (CFR).
2. Câmera: escala e posição por quadro (keyframes) sobre cada segmento.
3. Telas cheias por cima, no tempo delas.
4. Sobreposições (MOV transparente) por cima.
5. Legenda (MOV transparente) por cima de tudo, escondida onde o plano mandou.
6. Áudio: voz com crossfade de ~2 frames nas junções; sons nos tempos e níveis do bloco `sfx`; música só se horizontal/YouTube e a pessoa mandou (perfil). Normalizar para **-14 LUFS, pico ≤ -1 dBTP** (duas passadas do `loudnorm`).
7. Saída: MP4 H.264 (CRF ~18, `yuv420p`, `+faststart`), AAC 48 kHz 192 kbps, fps do vídeo, resolução cheia.

## Scripts
| Script | O que faz | Armadilhas |
|---|---|---|
| `final_render.py` | monta tudo pelo estado | aplicar câmera por quadro (ex.: `zoompan`/`scale`+`crop` com expressões, ou quadros via Python); conferir sincronia no fim do vídeo (erro de fps cresce); MOV com transparência como overlay (`format=yuva420p`) |
| `final_conferir.py` | duração, fps, loudness, 4–6 quadros-chave numa folha | — |

## Passo a passo
1. Rascunho rápido em 720 px para conferir sozinho (folha de quadros, sincronia boca/legenda num trecho).
2. Render final na resolução cheia, em segundo plano.
3. Conferir: duração, loudness, folha de quadros (legenda legível, animações no lugar, sem borda).
4. Enviar o MP4 final à pessoa (SendUserFile) com o lembrete: "para Reels/TikTok, adicione a música em alta no próprio app ao postar".

## Revisão
A pessoa pede pelo tempo do vídeo ("0:22 animação mais rápida", "0:30 som mais baixo"). Converta para o item (`mo`, `cam`, `sfx`, `lg`, `s`) e devolva para a etapa dona do item (ajuste direto se for pequeno). **Agrupe vários pedidos antes de renderizar de novo.** Nova versão sempre. Anote aprendizados.

## Aprovação
Marque `concluido`. Mostre quantos aprendizados ficaram no caderno e ofereça `/editar aprendizados` para levar ao perfil e às skills. Commit e push.

## Regras comuns
Antes de começar, leia `.claude/skills/editar/regras-comuns.md` (uma vez por sessão).
