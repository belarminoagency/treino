---
name: edit-cortes
description: "Faz o primeiro corte do vídeo: escolhe os takes, tira erros, pausas, 'ééé', repetições e notas de edição, e entrega um vídeo para a pessoa assistir no celular. Use em /edit-cortes, após a edit-preparar."
---

# edit-cortes

O corte limpo, com ritmo apertado. Sem legenda, zoom, animação ou som. Primeira revisão com vídeo: a pessoa assiste no celular.

- **Lê:** `transcricao/frases.txt`, `notas_edicao`, `silencios`, `_CLAUDE/roteiro.md`, perfil `estilo-cortes.md`.
- **Escreve:** bloco `cortes` (versão, segmentos `s001`… com bruto, início, fim no tempo do bruto, começo do texto), `marcadores`; `Renders/<projeto>_cortes_vNN.mp4` (leve, para revisão).
- **Próximo passo:** `/edit-legendas`

Se a `preparar` não estiver `concluido`, pare e sugira terminá-la.

## Ofício
- **Leia por frase, decida por frase.** Abra o arquivo por palavra só para um trecho, por script.
- **Takes:** frases repetidas ou parecidas, recomeços, frases abandonadas, "pera", "de novo". A pessoa lê o roteiro e improvisa: o roteiro ajuda a reconhecer a mesma frase dita duas vezes; um trecho que não está no roteiro **não** é erro.
- **Escolha do take:** (1) nota de edição; (2) o último take completo; (3) se o último tropeçou e um anterior está limpo, o anterior. Dois bons e escolha difícil: escolha um e marque o outro.
- Antes de descartar uma frase como incompleta, procure outro take dela que a transcrição tenha perdido.
- **Escolher e descartar entre ideias e takes, nunca no meio da frase.**
- **Pausas:** corta as consideráveis; ar entre frases conforme o perfil (apertado).
- **Hesitações:** corta só quando isolada por silêncio e longa. Colada na fala, fica e vira marcador.
- **Notas de edição:** o trecho inteiro sai.
- **Ordem:** a gravada. Reordenar, só sugerir (uma frase de impacto que funcionaria muito melhor como gancho).
- **Na dúvida, não corta e marca.**
- Corte final passou de ~65 s? Sugira onde enxugar (só sugerir).

## Perfil
`estilo-cortes.md`: ar entre frases, folga nas bordas, hesitações.

## Scripts
**Em uso (testado em 14/11/2026):** o Claude escreve `_CLAUDE/cortes/rascunho_vNN.json` (segmentos por índice de palavra em `palavras.json`, marcadores, folgas) → `~/.edicao-venv/bin/python edicao/ferramentas/cortes_bordas.py <pasta> <rascunho>` → `~/.edicao-venv/bin/python edicao/ferramentas/render_rascunho.py <pasta>` → enviar o MP4.
**Folgas aprovadas pela pessoa: `folga_ini` 0,18 s e `folga_fim` 0,20 s** (0,05/0,10 ficou picotado: "muitas pausas e cortes repentinos"). Se o corte mudar depois das outras etapas: guardar o bloco antigo em `_CLAUDE/cortes/cortes_vNN.json` e rodar `python3 edicao/ferramentas/remapear.py <pasta> <cortes_antigos.json>` (leva legenda, animações, câmera e sons para os tempos novos) e `~/.edicao-venv/bin/python edicao/ferramentas/recorte_atualizar.py <pasta> <cortes_antigos.json>` (recorte da pessoa).

| Script | O que faz | Armadilhas |
|---|---|---|
| `cortes_bordas.py` | ajusta cada borda pela energia do áudio + folga do perfil, arredonda para frames | não comer sílaba; muleta curta colada vira marcador, não fala afirmada |
| `render_rascunho.py` | monta os segmentos com FFmpeg num MP4 leve (720 px, H.264/AAC) | crossfade de áudio de ~2 frames em cada junção (sem estalo); cortar no frame exato (re-encode, não `-c copy`) |

## Passo a passo
1. Status e pendências desta etapa.
2. Ler as frases, decidir os segmentos (bruto, palavra inicial, palavra final) e os marcadores.
3. Ajustar bordas por script, gravar no estado (`cortes.versao` +1).
4. Renderizar o rascunho e **conferir antes de mandar**: duração, áudio sem estalo (ouvir não dá: conferir junções por pico/energia), quadros nas junções.
5. Enviar o vídeo para a pessoa (SendUserFile).

## Resumo no chat
Bruto → corte (duração), o que saiu (repetições, notas, pausas), marcadores em linguagem simples com o tempo do vídeo ("em 0:12 tinha dois takes bons, usei o segundo"). Marque `aguardando_aprovacao`, commit e push.

## Revisão
A pessoa pede pelo tempo do vídeo que assistiu ("em 0:15 tira essa frase", "volta o 'ééé' de 0:08"). Converta o tempo da sequência para o tempo do bruto pela lista de segmentos. Ajuste só o citado, nova versão, novo rascunho. Anote aprendizados no caderno. Se um ajuste dela contradiz algo que o Claude afirmou, reconheça.

## Aprovação
Marque `concluido` — **o corte trava.** Se mudar depois, avise que legendas, motion e câmera precisam ser recalculados. Diga quantos aprendizados ficaram anotados, commit e push, sugira `/clear` e `/editar`.

## Regras comuns
Antes de começar, leia `.claude/skills/editar/regras-comuns.md` (uma vez por sessão).
