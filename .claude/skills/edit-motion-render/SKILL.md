---
name: edit-motion-render
description: "Constrói e renderiza as animações aprovadas no plano (HyperFrames), busca logos e ícones e anota os eventos para o som. Use em /edit-motion-render, após a edit-motion-mapa."
---

# edit-motion-render

Constrói cada animação aprovada e renderiza. A etapa mais longa e a que mais depende do ofício.

- **Lê:** `motions` (plano aprovado), perfil `identidade.md`, `estilo-motion.md`, `catalogo.md`, peças-base em `edicao/ferramentas/pecas/`; `fluxo-de-edicao/guias/oficio-motion.md`, `hyperframes.md`, `etapa-motion-render.md` e, se precisar buscar logo/ícone, `etapa-assets.md`.
- **Escreve:** `_CLAUDE/motion/moNN/` (um projeto HyperFrames por item), `Renders/moNN_vNN.(mp4|mov)` (fora do git), `motions.itens[].render` e `_CLAUDE/motion/eventos.json` (para o som).
- **Próximo passo:** `/edit-camera` (ou `/edit-sfx` se narrado)

Se a `motion-mapa` não estiver `concluido`, pare e sugira terminá-la.

## Ofício (resumo; detalhes nos guias)
- **Versão do HyperFrames:** a mais nova no primeiro render do vídeo, **fixa no vídeo** (`ferramentas.hyperframes` no estado; todo comando `npx --yes hyperframes@<versão> …`).
- Tempo 0 = início do item na sequência; gatilho = `tempo_da_palavra − início`.
- **Tela cheia:** cena completa, fundo `#0B0B0F`, câmera virtual (aproximação + deriva em camadas separadas), chega em movimento, saída própria. **Sobreposição:** fundo transparente, só os elementos, lado oposto ao rosto. Marque a direção da saída (a câmera usa).
- Compor em 1080 de largura e renderizar na resolução do vídeo.
- **Ciclo por item:** `check` → `snapshot` nos momentos-chave e **olhar** (sobre um quadro do vídeo: legível, fora do rosto, área segura, sem brigar com a legenda) → render em fila, em segundo plano → conferir frames, resolução, transparência, última letra.
- **Eventos para o som** anotados na construção: chega, sai, bate, troca, clica, conta, revela — tempo, tipo em palavras livres, força, descrição.
- **Asset faltando:** construa com marcador visível ("FALTA: print da DM") e peça à pessoa. Logos/ícones públicos: buscar (Iconify e fontes oficiais), mostrar em **uma folha numerada**, respeitar licenças.
- **Peças-base:** a primeira vez que um elemento ficar bom (card de DM, número de lista, cartela), vira peça em `edicao/ferramentas/pecas/` (CSS + funções JS). Os próximos vídeos partem dela.

## Scripts
**Em uso (testado em 14/11/2026):** a pessoa prefere animações **atrás e em volta dela** (recortada na frente), não no peito.
- Uma composição só, no tempo da sequência: `_CLAUDE/motion/base/template.html` com `data-camada="tras|frente"` em cada item; gerar `tras/` e `frente/` com `sed s/__CAMADA__/<camada>/` e renderizar cada uma (`npx --yes hyperframes@<versão> render --format mov --fps 30 -o …`). GSAP e fontes ficam locais (`vendor/`, `fonts/`): o CDN jsdelivr é bloqueado.
- Recorte da pessoa: `python3 edicao/ferramentas/recorte_pessoa.py <pasta>` (~35 min na CPU para 35 s) → `_CLAUDE/midia/pessoa.mov`. **Sempre** passar ao final as caixas dos objetos parados da parede (`midia.objetos_parede` no estado; achar num quadro em que a pessoa não encosta neles): o modelo às vezes "pega" o objeto e ele aparece por cima da animação.
- Zona livre medida no quadro final: rosto x≈280–900, y≈360–1180; parede livre no alto (y<330) e dos lados.
- Saída de elemento que estava apagado parte da opacidade atual (senão pisca).
- `_CLAUDE/motion/eventos.json`: eventos para o som, anotados na construção.

## Revisão
Esta etapa não tem revisão com vídeo combinada: confira sozinho e mostre **uma imagem** com 1 quadro-chave por animação. A pessoa pode pedir por número ("mo04 mais rápido", "mo02 tira"). Feedback geral ("básico", "sem vida") pede refazer, não retocar. Revisão que muda duração → atualizar plano e estado. Anote aprendizados.

## Aprovação
Marque `concluido`. Padrão que funcionou → proponha entrar no `catalogo.md` do perfil (com o "sim" da pessoa). Commit e push (projetos HyperFrames sim; renders não). Sugira `/clear` e `/editar`.

## Regras comuns
Antes de começar, leia `.claude/skills/editar/regras-comuns.md` (uma vez por sessão).
