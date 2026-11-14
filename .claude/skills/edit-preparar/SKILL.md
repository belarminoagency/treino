---
name: edit-preparar
description: "Prepara o vídeo bruto para a edição: confere o arquivo, transcreve com o tempo de cada palavra, acha as pausas e as notas de edição faladas. Use em /edit-preparar, após a edit-iniciar."
---

# edit-preparar

Transforma o bruto em algo que o Claude consegue ler. Não corta nada (isso é da `cortes`).

- **Lê:** `projeto.json` (brutos, tipo, formato), `_CLAUDE/briefing.md`, `_CLAUDE/roteiro.md`.
- **Escreve:** blocos `midia`, `transcricao`, `silencios`, `notas_edicao` no estado; `_CLAUDE/transcricao/` (por palavra em JSON, por frase em texto legível), `_CLAUDE/audio/` (WAV, fora do git).
- **Próximo passo:** `/edit-cortes`

Se a `iniciar` não estiver `concluido`, pare e sugira terminá-la.

## Ambiente (toda sessão)
Rode `bash edicao/ferramentas/preparar_ambiente.sh`. Na primeira vez, escreva esse script: instala as dependências de `edicao/ferramentas/requirements.txt` (WhisperX e o que os scripts usarem) de forma idempotente, e confere ffmpeg, node e o Chromium. Sem GPU: WhisperX na CPU (`compute_type=int8`, modelo `large-v3` ou `medium` se ficar lento demais; anote o tempo gasto). Rode em segundo plano.

## Passo a passo
1. **Brutos presentes?** Se a sessão é nova e `Brutos/` não tem os arquivos, peça o reenvio.
2. **Inventário** (ffprobe por arquivo): duração, fps real (`r_frame_rate` e `avg_frame_rate`), resolução, rotação, codec, áudio.
   - **Celular grava com taxa de quadros variável (VFR)** com frequência: se `r_frame_rate` ≠ `avg_frame_rate`, converter para taxa constante (CFR) na taxa mais próxima (30 ou 60) numa cópia de trabalho `_CLAUDE/midia/bruto01_cfr.mp4`, e usar a cópia em todo o fluxo. Anote no estado.
   - **Espelhar:** se `espelhar` = true no estado, aplicar `hflip` na mesma cópia de trabalho (todo o fluxo usa a cópia; o bruto fica intacto).
   - **Vários brutos curtos** (celular grava um arquivo por take): ordenar pelo horário do nome/metadado; cada um vira uma cópia de trabalho própria.
   - **Rotação:** vídeo de celular pode vir com metadado de rotação; confira a largura/altura de exibição.
   - Alertas: sem áudio, ilegível, fps diferentes entre brutos.
3. **Áudio:** extrair WAV 16 kHz mono para transcrever (e o original 48 kHz para o render).
4. **Transcrição** (WhisperX, português, alinhamento por palavra, VAD):
   - passe como contexto os nomes e termos do briefing e do roteiro;
   - **confira o que foi engolido:** trechos com energia de áudio e sem palavra → retranscrever esses trechos sem o contexto inicial (o contexto às vezes faz o modelo inventar frases ou pular takes repetidos). Avise a `cortes`;
   - nunca troque o que foi falado pelo texto do roteiro (a pessoa improvisa em cima do roteiro: o improviso é conteúdo).
5. **Silêncios:** trechos sem fala acima de ~0,3 s (pelas palavras + `silencedetect` de apoio). Só mapear.
6. **Notas de edição** ("nota de edição" … "fim da nota"), tolerando variações da transcrição. Cada nota: início e fim (incluindo as expressões), texto, interpretação curta, etapa. Abertura sem fechamento: termina na próxima pausa ≥1 s, confiança baixa.
7. **Saída para o Claude ler:** `transcricao/frases.txt` — uma frase por linha, `[mm:ss.ss–mm:ss.ss] texto`, pausas longas marcadas `(pausa 0,8 s)`, notas marcadas. O arquivo por palavra é só para os scripts.
8. **Resumo no chat:** duração, fps (e se converteu), quantas frases, quantas notas, alertas. Marque `concluido` (esta etapa não precisa de aprovação, salvo alerta), commit e push, sugira `/clear` e `/editar`.

## Scripts
| Script | O que faz | Armadilhas |
|---|---|---|
| `preparar_ambiente.sh` | instala/confere tudo | idempotente; não reinstalar o que existe |
| `inventario.py` | ffprobe + VFR→CFR + rotação | `avg_frame_rate` vs `r_frame_rate`; manter o áudio intacto na conversão |
| `transcrever.py` | WhisperX + retranscrição dos buracos | contexto inicial só na 1ª passada; tempos no tempo do bruto |
| `notas.py` | acha as notas faladas | tolerar "nota da edição", "fim de nota" etc. |
| `tempo.py` | segundos ↔ frames com a taxa real | um lugar só para todos os scripts |

## Regras comuns
Antes de começar, leia `.claude/skills/editar/regras-comuns.md` (uma vez por sessão).
