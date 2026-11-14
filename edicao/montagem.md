# Montagem do fluxo de edição

Fase atual: 2 (entrevista) · Atualizado em 2026-11-14

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
- Notas faladas: <…>
- Animação: <…>
- Câmera: <…>
- Som: <…> (a pessoa tem interesse no Epidemic Sound; sons baixados pelo celular e enviados na sessão)
- Revisões: <…>
- Nomes: prefixo <…>; skill mestra /<…>

## Perfil
- <ainda não criado>

## Fluxo aprovado
<pendente>

## Skills escritas
- [ ] regras comuns

## Próximo passo
Entrevista, decisões 5 e 6: notas faladas e cortes.
