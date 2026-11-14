---
name: edit-motion-mapa
description: "Planeja as animações do vídeo (números grandes, cards, cartelas, telas) e a câmera em volta delas, e a pessoa aprova a lista pelo chat. Não anima nada. Use em /edit-motion-mapa, após a edit-legendas."
---

# edit-motion-mapa

A etapa que mais decide a qualidade. Planeja onde entra animação, o que mostra, como, e a intenção da câmera em volta. **Não anima nada**: propõe, ajusta com a pessoa e grava. Aprovação pelo chat, sem render.

- **Lê:** `cortes`, `legendas`, `briefing.md`, notas de edição; perfil `identidade.md`, `estilo-motion.md`, `estilo-camera.md`, `catalogo.md`; `fluxo-de-edicao/guias/oficio-motion.md` e `etapa-motion-mapa.md` (o guia completo desta etapa).
- **Escreve:** bloco `motions` (itens `mo01`… com tempo, formato, conceito, storyboard quando houver, palavras-gatilho, assets, câmera antes/durante/depois, onde a legenda some), `camera.batidas`.
- **Próximo passo:** `/edit-motion-render`

Se a `legendas` não estiver `concluido`, pare e sugira terminá-la.

## Ofício (resumo; detalhes no guia da etapa)
- **O conteúdo decide a animação**: a forma visual que explica *aquela* ideia; nada de template. O catálogo é repertório, nunca obrigação.
- Script gera a fala no **tempo da sequência**, uma frase por linha, com o tempo exato de cada corte.
- **Gancho primeiro (0–3 s) e com storyboard** (conceito, camadas, câmera, batidas, herói, vida, saída). Antes de mostrar: o conceito nasce desta fala? A energia combina? Estou repetindo a mesma fórmula?
- **Densidade média** (perfil): gancho com 1 animação forte; corpo 1 a cada ~5–8 s; chamada final.
- **Onde entra:** listas, números, comparação, antes/depois, exemplo concreto (DM, comentário), ferramenta citada, a frase-chave. **Onde não:** fala que se sustenta sozinha.
- **Formato:** tela cheia (cartela, mockup) ou sobreposição transparente. Lateral grande → câmera leva o rosto para o terço oposto.
- **Legenda:** marque onde ela some (tela cheia que já mostra a frase, animação que escreve o mesmo texto).
- **Duração:** mínimo ~2 s, típico 2–5 s em vídeo curto. Texto segura ~1 s depois da última palavra. Borda junto de corte → tempo exato do corte, não da palavra.
- **Câmera em volta**, em palavras: antes / durante / depois, e batidas fora das animações ("punch em 'nunca'"). Narrado: sem câmera.
- **Assets:** logo, print, gravação de tela, foto, B-roll (nos narrados). Peça o que faltar à pessoa ("me manda um print da sua DM"); logos e ícones públicos o render busca (ver `fluxo-de-edicao/guias/etapa-assets.md`: licenças). Não improvise com algo genérico.

## Revisão (pelo chat)
Mostre a lista numerada, uma linha por item: `mo01 · 0:00–0:03 · sobreposição · número "3" gigante azul atrás de você + ①②③ · câmera: punch no "três"`. Itens de asset que a pessoa precisa mandar em destaque. A pessoa aprova, ajusta ou risca por número. Ao regravar, preserve o status do que já foi aprovado. Anote aprendizados.

## Aprovação
Marque `concluido`, commit e push, sugira `/clear` e `/editar`.

## Regras comuns
Antes de começar, leia `.claude/skills/editar/regras-comuns.md` (uma vez por sessão).
