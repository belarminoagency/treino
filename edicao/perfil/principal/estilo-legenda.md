# Estilo de legenda — principal

O centro do estilo: presente nas 6 referências. Origem: refs 01–06 (fichas em `analises.md`).

## Blocos
- 1 a 3 palavras por bloco, quebradas nas pausas naturais da fala; nunca separar artigo/preposição da palavra seguinte ("a | renda" não).
- Troca de bloco seca, no tempo da primeira palavra do próximo bloco. (refs 01, 04)
- Sem pontuação, exceto "?" e "!" quando mudam o sentido.

## Posição
- Centro horizontal; altura do peito, ~62–68% da altura do quadro (vertical), nunca sobre o rosto. (todas)
- Área segura: 80% do quadro; no vertical, fora dos 15% de baixo (botões do Reels/TikTok) e dos 10% de cima.
- Horizontal (YouTube): ~75–80% da altura.

## Hierarquia
- Palavras de apoio: Inter 600, branco, ~44 px em 1080 de largura (vertical).
- Palavra-chave da frase (1 por frase, às vezes nenhuma): Inter Display 900, azul `#2F5BFF`, caixa alta, ~1,8–2,2× o tamanho do apoio, numa linha própria. (refs 01, 03, 05, 06)
- Ênfase especial rara: serifada itálica na cor de destaque. (refs 03, 04)
- Escolha da palavra-chave: o substantivo ou número que carrega a ideia ("TEMPO", "R$ 500", "PROSPECÇÃO"), não verbos genéricos.

## Movimento
- Entrada de cada palavra no tempo exato em que é dita: desfoque 8 px → 0 e opacidade 0 → 1 em ~6 frames (0,2 s), escala 0,92 → 1 em ~8 frames, `expo.out`. (refs 01, 04, 05: observado ~0,2–0,3 s)
- Palavra-chave: entra com punch leve (escala 1,15 → 1, ~10 frames, `back.out(1.6)`).
- A linha recentraliza a cada palavra nova (`power3.out`, ~0,3 s); nunca revelar sem recentralizar.
- Sem som na legenda comum (cansa).

## Quando a legenda some
- Durante cartela de tela cheia que já mostra a frase, e durante animação que escreve o mesmo texto.
