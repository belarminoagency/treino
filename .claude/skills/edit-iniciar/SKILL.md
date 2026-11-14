---
name: edit-iniciar
description: "Começa um vídeo novo: recebe o vídeo bruto e o roteiro que a pessoa mandou, cria a pasta do vídeo, o estado e o briefing. Use em /edit-iniciar, ou quando a pessoa mandar um vídeo novo para editar."
---

# edit-iniciar

Abre o projeto e organiza o briefing. Não analisa o vídeo (isso é da `preparar`).

- **Lê:** os arquivos que a pessoa mandou (`/root/.claude/uploads/...`), o perfil (só o nome).
- **Escreve:** `videos/<AAAA-MM-DD_Nome>/` (Brutos/, Assets/, Renders/, _CLAUDE/), `_CLAUDE/projeto.json`, `_CLAUDE/briefing.md`, `_CLAUDE/roteiro.md` (se houver), `_CLAUDE/aprendizados.md` vazio.
- **Próximo passo:** `/edit-preparar`

## Passo a passo
1. **Já existe?** Se a pessoa quer continuar um vídeo já iniciado, não sobrescreva: mostre o status e pergunte se é só para atualizar o briefing.
2. **Vídeo bruto:** se ainda não mandou, peça ("me manda o vídeo bruto aqui, pode ser mais de um arquivo"). Vários arquivos = vários takes/brutos, todos entram.
3. **Nome do vídeo:** sugira a partir do assunto, curto, sem acento e sem espaço (`2026-11-20_Prospeccao`). Data de hoje.
4. **Criar a pasta** e **copiar** os brutos para `Brutos/` (nunca mover o upload), com nomes simples (`bruto01.mp4`…), anotando no estado o nome original.
5. **Tipo e formato:** pergunte numa linha só, com sugestão: "É falando para a câmera ou narrado? Vai ser vertical (Reels/TikTok/Shorts) ou horizontal (YouTube)?" Se o bruto é vertical, sugira vertical.
   - **Espelhar** (virar esquerda ↔ direita): a pessoa pode pedir. Antes, olhe um quadro de cada bruto: texto, logo ou letreiro na cena sairia ao contrário — avise. Anote `espelhar: true/false` no estado; a `preparar` aplica na cópia de trabalho.
6. **Briefing:** "Me conta, do jeito que vier, sobre o que é esse vídeo e qualquer direcionamento que você já tenha." Organize sem inventar (preserve as palavras e a intenção): sobre o vídeo, direcionamentos gerais, observações por etapa. Omita seções vazias. Salve e mostre.
7. **Roteiro:** pergunte se tem roteiro; se tiver, que cole no chat ou mande o arquivo. Salve em `_CLAUDE/roteiro.md` sem mudar nada. Serve só para reconhecer takes e grafia de termos.
8. **Estado:** se `edicao/ferramentas/estado.py` não existir, escreva agora (ver "Scripts") e teste. Crie `projeto.json` com: projeto, perfil (`principal`), tipo (`apresentador`|`narrado`), formato (`vertical`|`horizontal`), brutos (nome, nome original), etapas (todas `pendente`; `camera` = `nao_precisa` se narrado), pendências vazias.
9. Marque `iniciar` = `concluido`, commit e push (sem os vídeos), e sugira `/clear` e `/editar`.

## Scripts
**Em uso (testado em 14/11/2026):** `python3 edicao/ferramentas/estado.py <pasta> status|<bloco>|--set|--etapa|--pendencia|--resolver`. A pasta do vídeo é `videos/<AAAA-MM-DD_Nome>/`; os brutos são copiados do upload para `Brutos/bruto01.mp4…` em ordem de horário.

| Script | O que faz | Armadilhas |
|---|---|---|
| `edicao/ferramentas/estado.py` | lê e muda o `projeto.json` sem abrir inteiro: `status`, `<bloco>`, `--json`, `--item`, `--set`, `--etapa`, `--pendencia`, `--resolver` | gravar de forma atômica (arquivo temporário + rename); `status` mostra alertas (ex.: `cortes.versao` mudou depois do `motion_mapa`); falta de brutos na sessão vira alerta |

## Regras comuns
Antes de começar, leia `.claude/skills/editar/regras-comuns.md` (uma vez por sessão).
