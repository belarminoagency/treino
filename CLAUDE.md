# Instruções para o Claude

## Fluxo de edição de vídeo (sessões na nuvem, pelo celular)
Quem usa este repositório trabalha com o Claude Code só pelo celular, em sessões na nuvem que são temporárias.
Tudo o que fica em `~/.claude/skills/` ou fora do repositório some quando a sessão acaba.

Por isso, ao usar a skill `fluxo-de-edicao` (e as skills que ela criar):
- Grave as skills geradas em `.claude/skills/<nome>/` **dentro deste repositório**, nunca em `~/.claude/skills/`.
  Onde os guias e modelos disserem `~/.claude/skills/`, leia como `.claude/skills/` deste repositório.
- Grave também aqui o perfil de estilo, as regras comuns e o caderno de aprendizados.
- Depois de criar ou mudar algo, faça commit e push para não perder o trabalho.
- Não há programa de edição no computador: prefira a opção "sem programa de edição" e entregue o vídeo renderizado,
  enviando o arquivo final para a pessoa baixar no celular.
- Vídeos brutos e renders não entram no repositório (são pesados). Ficam só na sessão.

## Continuidade entre computador e celular
Quem usa este repositório alterna entre o computador da empresa (às vezes com o Claude Code rodando localmente)
e o celular (sessões na nuvem). Conversas locais não aparecem no celular, então o repositório é a memória comum.

Em qualquer sessão, ao planejar ou construir automações (ou qualquer projeto com várias etapas):
- Mantenha um arquivo `planos/<nome-do-projeto>.md` com: objetivo, ferramentas usadas, decisões tomadas,
  o que já foi feito, próximos passos e pendências.
- Atualize esse arquivo a cada avanço importante e ao fim da conversa, e faça commit e push logo em seguida.
- Ao começar uma sessão, olhe a pasta `planos/` e retome o que estiver em andamento antes de recomeçar do zero.
- Nunca grave senhas, tokens ou chaves nesses arquivos.
