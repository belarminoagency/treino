---
name: edit-camera
description: "Desenha os movimentos de câmera no vídeo (zoom alternado nos cortes, punch nas ênfases, movimento casado com as animações). Use em /edit-camera, após a edit-motion-render. Vídeos narrados pulam esta etapa."
---

# edit-camera

O movimento da câmera sobre a filmagem, desenhado **depois** das animações prontas. Gera os valores de escala e posição por quadro, que a `final` aplica no render. Não renderiza o vídeo final.

- **Lê:** `cortes`, `motions` (tempos, formato, direção de saída, intenção de câmera), `camera.batidas`, perfil `estilo-camera.md`; `fluxo-de-edicao/guias/etapa-camera.md` e `oficio-motion.md` §2–§4.
- **Escreve:** bloco `camera` (movimentos `cam01`… e a base), `_CLAUDE/camera/keyframes.json` (escala e posição por quadro), eventos de câmera para o som.
- **Próximo passo:** `/edit-sfx`

Se a `motion-render` não estiver `concluido`, pare e sugira terminá-la. Vídeo narrado: marque `nao_precisa` e siga.

## Ofício (resumo; detalhes no guia)
- **Base por script:** a cada corte, alterna aberto 100% ↔ fechado (perfil: ~115%); aproximação lenta por baixo (+3–5% por segmento) numa camada própria; o plano do corte é escolhido por onde a câmera terminou no take anterior; o primeiro segmento começa aberto; corte com mudança < 5% gera aviso.
- **Casar com as animações:** acelera para dentro (`power4.in`, 0,2 s) antes de animação que entra no corte; chega na direção da saída (`expo.out`, 0,4–0,6 s) depois; sobreposição lateral leva o rosto ao terço oposto e devolve; sob tela cheia, nada.
- **Punch** na palavra de ápice: +6%, assenta em ~0,3 s. Variar as formas, não repetir em sequência.
- **Cuidados:** nada de salto de escala no meio de um take visível; todo movimento parte de onde a câmera está; não inverter direção no corte; olhos a ~35% da altura no plano fechado; nunca mostrar borda do quadro; uma coisa por vez em cada camada.
- **Rosto:** detector YuNet (OpenCV) no vídeo de trabalho, resultado em cache em `_CLAUDE/camera/rosto.json` — para enquadrar olhos e para adaptar formato.

## Scripts
| Script | O que faz | Armadilhas |
|---|---|---|
| `camera_rosto.py` | YuNet a cada N quadros, suavizado | cache; quadros escuros |
| `camera_calc.py` | base + movimentos → keyframes por quadro, com as curvas; avisos de conflito e borda | limitar deslocamento pela margem; `tempo.py` |
| `camera_preview.py` | aplica os keyframes no corte (sem legenda/motion) em vídeo leve | só para o Claude conferir |

## Passo a passo
1. Rascunho com os movimentos numerados (o quê, onde, duração, curva, de quanto a quanto).
2. Calcular, resolver avisos, gerar preview e **conferir sozinho** por quadros (borda, olhos, saltos).
3. Resumo curto à pessoa (quantos movimentos, os principais em uma linha cada). Sem vídeo nesta etapa (a revisão com vídeo é a final), salvo se ela pedir.

## Revisão
Por número: "cam07 mais lento", "cam05 mais forte", "cam12 tira". Se uma animação mudar depois, recalcular. Anote aprendizados.

## Aprovação
Marque `concluido`, commit e push, sugira `/clear` e `/editar`.

## Regras comuns
Antes de começar, leia `.claude/skills/editar/regras-comuns.md` (uma vez por sessão).
