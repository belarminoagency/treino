---
name: editar
description: "Ponto de entrada da edição de vídeo: mostra onde o vídeo está (etapas, pendências, aprendizados anotados) e abre a skill da etapa certa. Também começa um vídeo novo quando a pessoa manda um vídeo bruto, e aplica os aprendizados (/editar aprendizados). Use em /editar, ao abrir ou retomar um vídeo, depois de um /clear, ou quando a pessoa perguntar em que pé está o vídeo."
---

# editar

Fluxo: iniciar → preparar → cortes → legendas → motion-mapa → motion-render → camera → sfx → final

Antes de tudo, leia `regras-comuns.md` (nesta pasta), uma vez por sessão.

## /editar
1. **Qual vídeo:** liste `videos/*/_CLAUDE/projeto.json` no repositório.
   - Nenhum, ou a pessoa mandou um vídeo novo: diga que o vídeo ainda não foi iniciado e ofereça a `/edit-iniciar`.
   - Mais de um em andamento: pergunte qual (pelo nome e data).
2. **Status:** rode `python3 edicao/ferramentas/estado.py <pasta> status` e mostre de forma curta: etapas, pendências, alertas e quantos aprendizados estão anotados. Se os brutos não estiverem na sessão (sessão nova), diga isso e peça o reenvio antes de seguir.
3. **Próximo passo:** diga qual é e pergunte se segue. Com o "sim", abra a skill da etapa (`/edit-<etapa>`) e siga as instruções dela.
   - Etapa aguardando revisão: o próximo passo é continuar essa mesma etapa, nunca pular.
   - Alerta de algo desatualizado (ex.: o corte mudou depois do plano de animação): mostre primeiro e espere a decisão.
   - Vídeo narrado: a etapa `camera` fica `nao_precisa`.
4. **Uma etapa por vez.** Não encadear etapas sozinho e não dar `/clear` (isso é sempre da pessoa).
5. **Modelo:** lembre, numa linha, o modelo sugerido para a etapa. Trocar logo depois do `/clear` não custa nada.

| Etapa | Modelo | Esforço |
|---|---|---|
| editar, iniciar | o mais leve que funcione bem | baixo |
| preparar, legendas, final | intermediário | médio |
| cortes, motion-mapa, motion-render, camera | o mais capaz | alto |
| sfx, aplicar aprendizados | o mais capaz | médio |

## /editar aprendizados
Siga a seção 5 das regras comuns.

## Regras
- Não editar vídeo nem rodar scripts de etapa: isso é das skills de cada etapa.
- Nunca mover, renomear ou apagar arquivos que a pessoa mandou.
