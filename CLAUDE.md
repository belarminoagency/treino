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
