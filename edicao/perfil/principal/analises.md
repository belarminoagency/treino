# Fichas das referências

Analisadas em 2026-11-14. Todas verticais 720x1280. Os arquivos .mp4 ficam fora do git (só na sessão); estas fichas são o que fica.
Método: folhas de contato a 1 quadro/s, folhas densas a 10 quadros/s nos trechos de texto, detecção de cortes (ffmpeg scene > 0.3), loudness (EBU R128).
Ainda não medido: curvas exatas por fluxo óptico (fazer quando houver os scripts de medição). Os tempos abaixo são observados nas folhas densas.

| Ref | Duração / fps | Tipo | Cortes de cena | Loudness |
|---|---|---|---|---|
| ref01 | 82,8 s / 30 | apresentador sentado, muito motion | 9 (planos de tela/ilustração) | -14,5 LUFS |
| ref02 | 42,4 s / 30 | apresentador + telas de celular (tutorial) | 10 | -14,1 LUFS |
| ref03 | 15,0 s / 24 | trecho de podcast, cartelas tela cheia | 5 | -14,9 LUFS |
| ref04 | 19,6 s / 30 | apresentador de frente, só legenda | 6 (jump cuts) | -14,2 LUFS |
| ref05 | 17,1 s / 23,976 | entrevista, legenda minimalista | 3 | -20,9 LUFS |
| ref06 | 30,3 s / 25 | institucional, apresentador + B-roll | 16 (~1 a cada 1,5–2 s) | -17,5 LUFS |

## ref01 — prospecção ativa
- Legenda em blocos de 1–3 palavras, palavra-chave grande em azul saturado (#1E4BFF aprox.) com contorno/sombra, palavras de apoio pequenas em branco.
- Texto entra em ~0,2–0,3 s (6–9 frames) com desfoque + escala, assenta e fica; risco (strike) animado sobre palavra ("prospecção" riscada em vermelho).
- Grandes números 3D ("1º", "3º", "7") atrás/acima do apresentador, ficam vários segundos enquanto ele explica o item.
- Cards de interface (DM, comentários, avatares em círculo) entram por cima; tela cheia escura com mockup de conversa.
- Câmera: punch-ins visíveis (14–15 s) e plano mais fechado em momentos de ênfase.

## ref02 — 3 truques (tutorial de app)
- Paleta: fundo escuro + verde-limão neon (#C6FF3A aprox.). Numeração grande "1/2/3" com indicador de progresso ①–②–③ no topo.
- Grande parte do vídeo é mockup de celular inclinado com gravação de tela, sobre fundo escuro com brilho verde; destaque (contorno verde) no item da tela.
- Ícones em selo arredondado (amarelo-limão) ao lado do texto.

## ref03 — podcast "quando tudo sai do controle"
- Palavra-chave em serifada dourada grande; palavras de apoio em sans pequena acima.
- Cartelas tela cheia em fundo preto/cinza ("RAZÃO" com brilho dourado, "SÓ RAZÃO / ZERO EMO") — escrita letra a letra.
- Desfoque forte do fundo na transição para a cartela. Legenda comum: 1 palavra, branca, pequena, no peito.

## ref04 — "falta tempo"
- Só legenda, 1–3 palavras por vez, branca, sans bold, centro-baixo (altura do peito).
- Ênfase: palavra em itálico serifado vermelho ("desculpa"); palavras entram com desfoque (blur → nítido).
- Câmera: zoom alternado nos jump cuts (enquadramento muda de tamanho a cada corte, ex.: 6 s, 16–17 s). Fundo escuro, look cinematográfico.

## ref05 — "ganhar mais dinheiro"
- Legenda minimalista, palavra por palavra acumulando na linha (cada palavra surge em ~0,1–0,2 s, cinza → branco); a palavra final da frase entra maior e em negrito ("a renda.", "maiores", "preparadas.").
- Fade para preto/escurecido em frase de impacto ("a própria capacidade."); flash branco de 1 quadro como transição (11 s).
- Tom cinematográfico, áudio mais baixo (-20,9 LUFS), sem efeitos chamativos.

## ref06 — institucional (embalagens)
- Laranja de marca (#E8650F aprox.) em cartela tela cheia e no risco animado sobre palavra ("erro", "comprometer").
- B-roll trocando a cada 1–2 s enquanto a voz continua; volta ao apresentador nas frases-chave. Encerramento com logo sobre fundo desfocado.
- Legenda pequena, branca, 1–2 palavras, com palavra-chave maior.
