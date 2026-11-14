---
name: edit-sfx
description: "Coloca os efeitos sonoros (whoosh, pop, clique, impacto) alinhados com as animações, a câmera e os cortes, e cuida da biblioteca de sons. Use em /edit-sfx, após a edit-camera (ou a motion-render, se narrado)."
---

# edit-sfx

O som entra por último, sobre corte, legendas, animações e câmera travados. Decide onde entra som, qual e como se empilha. A `final` mixa.

- **Lê:** eventos (`motion/eventos.json`, câmera, cortes), `motions` (ideia e storyboard), perfil `estilo-som.md`, `edicao/sons/indice.json`; `fluxo-de-edicao/guias/etapa-sfx.md`.
- **Escreve:** bloco `sfx` (itens `sfx01`… com evento, camada, arquivo, alinhamento, nível), sons novos na biblioteca (se a pessoa mandou).
- **Próximo passo:** `/edit-final`

Se a etapa anterior não estiver `concluido` (ou `nao_precisa`), pare e sugira terminá-la.

## Biblioteca (`edicao/sons/`)
- Pastas por categoria: `whoosh/`, `impacto/`, `grave/`, `riser/`, `pop/`, `clique/`, `glitch/`, `interface/`, `ding/`. Índice gerado por script (`sons_indice.py`): duração útil, **tempo até o pico**, forma, brilho, favoritos.
- **Primeira vez:** gerar uma base com `sons_sintetizar.py` (numpy/ffmpeg: whooshes de ruído filtrado com envelope, pops, cliques, impactos com sub, risers), 3–5 variações por categoria, normalizadas, WAV 48 kHz. Sem problema de licença. Ouvir não dá: conferir forma de onda e espectro.
- **Sons da pessoa (Epidemic Sound etc.):** chegam pelo upload → conferir, cortar silêncio inicial, padronizar (WAV 48 kHz), separar por categoria, atualizar o índice, commit (arquivos de som são leves; ajustar o `.gitignore` se precisar para `edicao/sons/**`). Sons ainda sem categoria → pasta `entrada/`.
- Faltou som bom? Não force um ruim; anote em `edicao/sons/faltando.md` e sugira à pessoa o que baixar ("whoosh curto e grave").

## Ofício (resumo; detalhes no guia)
- **O som segue o que se vê.** Jump cut sem mudança de plano: sem som. Sob tela cheia, câmera não pede som. Legenda comum: sem som.
- Um protagonista por momento; no máximo 3 camadas (principal, grave só nos fortes, doce curto).
- Respiro antes do impacto; escalada: o maior impacto no ápice do gancho.
- **Sincronia:** impacto no frame do evento; whoosh com o **pico** na chegada/troca; pop e clique começam no evento.
- Não repetir o mesmo arquivo em ~20 s. Nível pela loudness da voz (alvos no perfil).

## Scripts
**Em uso (testado em 14/11/2026):** biblioteca gerada por `~/.edicao-venv/bin/python edicao/ferramentas/sons_sintetizar.py` + índice `sons_indice.py` (`edicao/sons/indice.json`). O Claude escreve `_CLAUDE/sfx/plano_vNN.json` (id, evento, camada, arquivo, `t`, `alinha` pico|inicio, `db` relativo ao pico da voz); o `final_render.py` posiciona e mixa. O Claude **não ouve** o áudio: peça à pessoa para conferir os sons. "Buh" que a pessoa escrever pode ser "bug": pergunte antes de mexer no som.

## Passo a passo
1. Script junta os eventos no tempo da sequência (id estável, palavra dita, loudness da voz).
2. Rascunho: para cada som, evento, camada, arquivo, alinhamento.
3. Script posiciona, nivela e avisa (não achado, repetido, colado).
4. Resumo curto à pessoa: quantos sons, onde estão os principais. Sem vídeo nesta etapa (vai na final).

## Revisão
"sfx12 mais baixo" (−3 dB), "sfx05 tira", "troca o sfx07", "sfx03 um frame antes". Anote aprendizados.

## Aprovação
Marque `concluido`, commit e push, sugira `/clear` e `/editar`.

## Regras comuns
Antes de começar, leia `.claude/skills/editar/regras-comuns.md` (uma vez por sessão).
