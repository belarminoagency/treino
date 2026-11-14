# Regras comuns das skills edit-*

Lidas uma vez por sessão por todas as skills de edição. Mudou uma regra geral? Mude aqui, não em cada skill.

Repositório: `/home/user/treino` (ou a raiz do repositório `treino` na sessão).
Ferramentas: `edicao/ferramentas/` (scripts; dependências Python em `requirements.txt`).
Perfil: `edicao/perfil/<nome>/` (o nome vem do estado do vídeo; hoje só existe `principal`).
Sons: `edicao/sons/`.
Vídeos: `videos/<AAAA-MM-DD_Nome>/` com `Brutos/`, `Assets/`, `Renders/` e `_CLAUDE/`.

## 0. Ambiente na nuvem (ler primeiro)
- A pessoa usa só o celular, pelo app do Claude. A sessão roda num servidor temporário: **tudo fora do git some quando a sessão acaba.**
- Vai para o git: skills, perfil, scripts, sons da biblioteca, `_CLAUDE/projeto.json`, `_CLAUDE/aprendizados.md`, briefing e textos. **Não vai:** vídeo, áudio, renders e frames (pesados; o `.gitignore` cuida). Confira com `git status` antes de cada commit.
- **Commit e push ao fim de cada etapa** (e depois de cada revisão aplicada), para a próxima sessão achar o estado. Branch: a de trabalho da sessão, e depois `main`, se a pessoa autorizou (já autorizou enviar direto para o `main` em 14/11/2026).
- Arquivos enviados pela pessoa chegam em `/root/.claude/uploads/<sessão>/...`. Copiar (nunca mover) para a pasta certa do vídeo.
- **Sessão nova no meio de um vídeo:** o estado está no git, mas os brutos e renders não. Antes de qualquer etapa que use mídia, conferir se `Brutos/` tem os arquivos listados em `projeto.json` (nome e duração). Se faltar, pedir para a pessoa reenviar o vídeo bruto. Renders intermediários são refeitos pelos scripts a partir do estado.
- Ferramentas que não estão no servidor (transcrição, pacotes Python, HyperFrames) são instaladas pelo script `edicao/ferramentas/preparar_ambiente.sh` (criado na primeira vez que a etapa preparar rodar). Rodar no começo de toda sessão que vai editar.
- Sem GPU: transcrição e render na CPU. Tarefas longas em segundo plano.
- **Entregar vídeo para a pessoa:** com a ferramenta de enviar arquivo (SendUserFile), sempre MP4 H.264 + AAC, que abre em qualquer celular. Para revisão, versão leve (720 px de largura); o final, na resolução cheia.

## 1. Conversa e segurança
- Português, frases curtas, sem jargão. Uma pergunta por vez, sempre com a sugestão.
- Nunca mover, renomear ou apagar os arquivos que a pessoa mandou. Tudo o que o Claude gera fica em `_CLAUDE/` ou `Renders/`.
- Nunca sobrescrever um arquivo já entregue: versão nova (`_v01`, `_v02`…).

## 2. Estado do vídeo sem ler inteiro
O `_CLAUDE/projeto.json` cresce muito. Ler e mudar sempre pelo script `edicao/ferramentas/estado.py` (criado na etapa iniciar):
- `estado.py <pasta> status` mostra onde o vídeo está;
- `estado.py <pasta> <bloco>` mostra o resumo de um bloco (`--json` para o bloco inteiro);
- `--item <id>` mostra um item;
- `--set <caminho> <valor>` muda um campo solto;
- `--etapa <etapa>=<status>` muda o status de uma etapa;
- `--pendencia <etapa> "<texto>"` anota uma pendência, e `--resolver <id>` a resolve.
Status: `pendente`, `em_andamento`, `aguardando_aprovacao`, `aguardando_pessoa`, `concluido`, `nao_precisa`.
Tempos de corte e marcadores ficam no tempo do arquivo bruto; ids estáveis (`s001`, `lg01`, `mo04`, `cam07`, `sfx12`).

## 3. Caderno de aprendizados (`_CLAUDE/aprendizados.md`)
Anotar na hora, durante a revisão de qualquer etapa, toda correção, elogio ou preferência que vale para outros vídeos:
- "zoom mais sutil", "esse som ficou ótimo": **anota**;
- "tira essa frase": **não anota** (é só deste vídeo);
- na dúvida, anota com "(talvez só deste vídeo)".
Formato: `- [ ] <etapa> · <o que foi pedido, com contexto> · <dd/mm>`. Depois de aplicado: `- [x] … → <onde entrou>`; só daquele vídeo: `- [-] …`. Nunca apagar linhas. Anotar não é mudar: as skills e o perfil só mudam quando a pessoa pedir (seção 5).

## 4. Ponto salvo e fechar uma etapa
- Os vídeos têm 30–60 s: cada etapa trabalha o vídeo inteiro de uma vez (sem trechos).
- **Ponto salvo:** etapa terminada, revisões aplicadas, entrega gerada, commit e push feitos. Só aí sugerir `/clear` e `/editar`.
- **Pendência:** pedido ainda não aplicado é anotado na hora pelo script de estado e aparece no status.
- **Fechar a etapa** (aprovada): marcar `concluido`, dizer quantos aprendizados ficaram anotados, commit e push, sugerir `/clear` e `/editar`.
- Revisões com o vídeo (3 pontos combinados): depois dos cortes, plano de animações pelo chat, vídeo final. Nas outras etapas, a pessoa não precisa assistir; o Claude confere sozinho por quadros e segue quando ela disser "sim".

## 5. Aplicar os aprendizados (quando a pessoa pedir)
1. Ler as linhas `- [ ]` do caderno.
2. Propor onde cada uma entra: gosto vai para o perfil (`identidade.md`, `estilo-*.md`, `catalogo.md`); ofício (vale para qualquer vídeo) vai para a skill da etapa; o que vale para todas as etapas vai para este arquivo.
3. A pessoa filtra. Gravar só o aprovado, mostrando antes o texto das mudanças maiores. Marcar cada linha. Commit e push.

## 6. Scripts
- O Claude decide sobre o texto; os scripts fazem as contas (tempos, frames, bordas, níveis, render).
- Um script nasce na primeira vez que a etapa roda num vídeo real, é testado e fica em `edicao/ferramentas/` para os próximos. Anotar o uso na skill da etapa.
- Conversão segundos → frames num lugar só (`edicao/ferramentas/tempo.py`), com a taxa real do vídeo (29,97 ≠ 30; celular costuma gravar com taxa variável: ver etapa preparar).
- Mudou um script que já funcionava? Comparar o resultado com o de antes no mesmo vídeo.
