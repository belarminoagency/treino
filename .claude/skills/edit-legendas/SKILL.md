---
name: edit-legendas
description: "Cria a legenda dinâmica do vídeo: blocos de 1 a 3 palavras sincronizados com a fala, com a palavra-chave grande em azul. Use em /edit-legendas, após a edit-cortes."
---

# edit-legendas

A legenda dinâmica é o centro do estilo (está nas 6 referências). Esta etapa decide os blocos e as palavras-chave e renderiza a legenda como uma camada transparente. Não faz outras animações.

- **Lê:** `cortes` (segmentos travados), transcrição por palavra (só pelos scripts), perfil `estilo-legenda.md` e `identidade.md`.
- **Escreve:** bloco `legendas` no estado (blocos `lg01`… com tempo da sequência, palavras e destaque), `_CLAUDE/legendas/` (projeto HyperFrames), `Renders/<projeto>_legendas_vNN.mov` (fora do git).
- **Próximo passo:** `/edit-motion-mapa`

Se a `cortes` não estiver `concluido`, pare e sugira terminá-la.

## Ofício
- Script converte as palavras para o **tempo da sequência** (pelos segmentos) e propõe blocos de 1–3 palavras nas pausas naturais. O Claude revisa a lista em texto: quebras que separam artigo/preposição, grafia (nomes e termos do roteiro e do briefing), números ("quinhentos reais" → "R$ 500").
- **Palavra-chave:** no máximo 1 por frase, às vezes nenhuma. O substantivo ou número que carrega a ideia. Ênfase especial (serifada itálica) no máximo 1–2 por vídeo.
- Cada palavra entra no tempo exato em que é dita; o bloco troca seco no tempo da primeira palavra do próximo.
- Palavra cortada pela borda de um segmento: a legenda segue o tempo da sequência, nunca mostra palavra que saiu do corte.

## Perfil
`estilo-legenda.md` (blocos, posição, hierarquia, movimento) e `identidade.md` (cores, fontes).

## Scripts
**Em uso (testado em 14/11/2026):** `python3 edicao/ferramentas/legendas_blocos.py <pasta>` (proposta) → o Claude revisa `blocos.json` (quebras, `destaque`, `enfase`, juntar palavras-chave como "todos os dias") → `legendas_blocos.py <pasta> --gravar` → `python3 edicao/ferramentas/legendas_render.py <pasta> --check|--snapshot t1,t2|--render`. Prévia sobre o vídeo: `python3 edicao/ferramentas/quadro_seq.py <pasta> <t> <saida.png> [legenda.png]`. Posição aprovada: y≈1460 (no peito; o rosto deste enquadramento desce até ~1050).

| Script | O que faz | Armadilhas |
|---|---|---|
| `legendas_blocos.py` | palavras → tempo da sequência → blocos propostos (JSON + texto legível) | usar `tempo.py`; palavra na borda de corte |
| `legendas_render/` (peça-base HyperFrames) | um `index.html` que lê o JSON de blocos e anima conforme o perfil | ver `fluxo-de-edicao/guias/hyperframes.md`: `fromTo` + `lazy:false`, fontes embutidas, `document.fonts.ready`, duração `(N − 0,5)/fps`; recentralizar a linha a cada palavra |

Primeira vez: construir a peça-base, `check`, snapshots em 3 momentos sobre um quadro do vídeo, mostrar à pessoa **uma imagem** antes de renderizar tudo. A peça-base fica em `edicao/ferramentas/legendas_render/` para os próximos vídeos.

## Passo a passo
1. Gerar os blocos, revisar o texto, escolher palavras-chave.
2. Render da camada transparente (MOV ProRes 4444) na resolução do vídeo, em segundo plano.
3. Conferir: frames = duração da sequência; 3 quadros compostos sobre o vídeo (texto legível, fora do rosto, dentro da área segura).
4. Mostrar à pessoa 2–3 quadros compostos numa imagem só (não precisa vídeo nesta etapa) e a lista de palavras-chave.

## Resumo no chat
Quantos blocos, quais palavras-chave em azul (lista curta) e a imagem. Marque `aguardando_aprovacao`, commit e push.

## Revisão
"tira o destaque de X", "destaca Y", "lg07 escreve Z". Ajuste, nova versão. Anote aprendizados (ex.: "legenda menor").

## Aprovação
Marque `concluido`, commit e push, sugira `/clear` e `/editar`.

## Regras comuns
Antes de começar, leia `.claude/skills/editar/regras-comuns.md` (uma vez por sessão).
