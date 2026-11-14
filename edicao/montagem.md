# Montagem do fluxo de edição

Fase atual: 6 (teste num vídeo curto) · Atualizado em 2026-11-14

## Ambiente
- Sessão na nuvem (Claude Code pelo app do celular), temporária: tudo o que precisa ficar vai para este repositório.
- Sistema: Linux · Python: 3.13 · FFmpeg: 6.1 · Node.js: 22 · Chromium: pré-instalado · GPU: não tem
- Instalado nesta montagem: nada ainda (transcrição pendente)

## Decisões
- Revisão: vídeo pronto (sem programa de edição; a pessoa revisa no celular e pede ajustes pelo chat)
- Tipo e formato: principal = falando para a câmera; às vezes vídeo narrado (voz sobre imagens). Vertical 9:16 (Reels/TikTok/Shorts) agora; horizontal 16:9 (YouTube) em breve, então o formato é escolhido por vídeo. Grava com a câmera do celular (resolução e fps lidos do arquivo em cada vídeo, nunca supostos).
- Duração típica: 30 s a 1 min (curtos: o fluxo trabalha o vídeo inteiro de uma vez, sem dividir em trechos)
- Pastas: ferramentas em `edicao/` (neste repositório). Cada vídeo numa pasta da sessão `videos/AAAA-MM-DD_Nome/` com `Brutos/`, `Assets/`, `Renders/` e `_CLAUDE/` (estado); vídeos e renders fora do git. O estado (`_CLAUDE/*.json`) e o caderno de aprendizados vão para o repositório.
- Transcrição: WhisperX local, na CPU (gratuita; reinstalada a cada sessão até existir script de preparação do ambiente). Alternativa futura: ElevenLabs Scribe.
- Notas faladas: "nota de edição" … "fim da nota" (sugestão padrão, aceita sem objeção)
- Cortes: ritmo apertado (tira pausas, "ééé", "hum", respirações longas e repetições); na dúvida não corta e pergunta. Grava com roteiro mas improvisa em cima: o roteiro serve para reconhecer takes repetidos e a grafia de termos, nunca para trocar o que foi falado; o improviso é conteúdo válido, não erro.
- Animação: sim, HyperFrames. Densidade média, "o necessário": mais no gancho (primeiros ~3 s), ênfases nas palavras-chave no meio, algo na chamada final. Maioria sobreposição; tela cheia de vez em quando (mais nos narrados).
- Câmera: zoom alternado nos cortes (disfarça o jump cut) + punch nas ênfases + câmera casada com as animações (feita depois das animações prontas). Seguir o rosto só quando precisar adaptar formato (vertical ↔ horizontal). Vídeos narrados pulam a etapa. A pessoa deixou o gosto fino a critério do Claude.
- Som: efeitos sonoros pelo Claude. Biblioteca em `edicao/sons/` por categoria (whoosh, pop, clique, impacto, riser…): começa com sons sintetizados por código (sem problema de licença); depois cresce com sons do Epidemic Sound que a pessoa baixa no celular e envia (guardados uma vez no repositório). Música: Reels/TikTok/Shorts SEM música no render (a pessoa adiciona música em alta no app ao postar); YouTube: trilha de fundo baixa, enviada pela pessoa.
- Revisões: (1) vídeo só com os cortes, assistido no celular; (2) plano das animações aprovado pelo chat (lista com tempos), sem render; (3) vídeo final completo (animações + câmera + som). Correções pelo chat citando o tempo ("0:15 corta essa frase") ou o número do item.
- Nomes: prefixo `edit-`; skill mestra `/editar`

## Perfil
- principal (`edicao/perfil/principal/`): confirmado. Branco + azul elétrico #2F5BFF, Inter. Legenda dinâmica é o centro do estilo. Falta: logo/@ (opcional); medir curvas por fluxo óptico.

## Fluxo aprovado (14/11/2026)
- /editar — skill mestra: mostra onde o vídeo está e chama a etapa certa
1. edit-iniciar — recebe o bruto e o roteiro, cria a pasta, o estado e o briefing
2. edit-preparar — inventário (VFR→CFR), transcrição por palavra, pausas, notas faladas
3. edit-cortes — corte apertado → revisão 1 (vídeo no celular)
4. edit-legendas — legenda dinâmica com palavra-chave azul
5. edit-motion-mapa — plano das animações e da câmera → revisão 2 (pelo chat)
6. edit-motion-render — animações no HyperFrames (assets dentro desta etapa)
7. edit-camera — zoom alternado, punch, casada com as animações (narrado: pula)
8. edit-sfx — efeitos sonoros + biblioteca
9. edit-final — junta tudo, -14 LUFS, entrega o MP4 → revisão 3

## Skills escritas (em `.claude/skills/`)
- [x] regras comuns (`editar/regras-comuns.md`)
- [x] editar · [x] edit-iniciar · [x] edit-preparar · [x] edit-cortes · [x] edit-legendas
- [x] edit-motion-mapa · [x] edit-motion-render · [x] edit-camera · [x] edit-sfx · [x] edit-final
- Perfil dividido em `edicao/perfil/principal/` (identidade, estilo-legenda, estilo-motion, estilo-camera, estilo-cortes, estilo-som, catalogo)
- Scripts: nascem no teste (fase 6)

## Próximo passo
Fase 6: teste com um vídeo curto (30–60 s) da pessoa, rodando /editar do começo ao fim. Depois: salvar script de preparação do ambiente (setup script) para as próximas sessões.
