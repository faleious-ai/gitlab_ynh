# Registro de decisões

## Uso

Este arquivo é o índice operacional. Decisões duráveis possuem ADR próprio. Decisões locais de uma rodada ficam no round record e só são promovidas quando alteram contrato, arquitetura, autoridade, risco ou continuidade.

## Estados

- `PROPOSED`: ainda não autoriza execução dependente.
- `ACCEPTED`: vigente.
- `SUPERSEDED`: substituída.
- `REJECTED`: considerada e recusada.

## Decisões vigentes

| ID | Estado | Decisão | Autoridade |
|---|---|---|---|
| ADR-0001 | SUPERSEDED_BY_ADR-0006 | desenvolvimento direto em `master`; política antiga de um commit por rodada substituída | usuário |
| ADR-0002 | ACCEPTED | repositório e evidência persistida prevalecem sobre contexto de chat | MAESTRO + usuário |
| ADR-0003 | ACCEPTED | “latest” é descoberta de versão elegível com pin de URL/hash, nunca resolução dinâmica em instalação | supply chain |
| ADR-0004 | ACCEPTED | agentes decidem tecnicamente dentro do mandato; humano decide gates de missão, risco e irreversibilidade | usuário |
| ADR-0005 | ACCEPTED | ChatGPT orquestra/revisa; Codex executa charters completos, usa subagentes e não aceita o próprio trabalho | usuário |
| ADR-0006 | ACCEPTED | rodada autoriza; tarefa implementa, versiona e reverte; síntese MAESTRO–Cavekit com TDD, backprop, revisão adversarial, compressão limitada e convergência | usuário |

## Decisões operacionais derivadas

- `gitlab_ynh` é coordenador temporário até existir `gitlab-mcp`.
- `gitlab-runner_ynh` mantém autoridade local sobre implementação, testes e skills de execução do Runner.
- `Leia AGENTS.md e continue` autoriza apenas o charter `READY`.
- O orquestrador elimina perguntas humanas materiais antes de liberar o charter.
- Backprop técnico e demais decisões reversíveis pertencem ao mandato autônomo.
- O Codex conclui tarefas não bloqueadas e continua frentes independentes antes de escalar.
- Subagentes não fazem commit nem integração final.
- Cada tarefa concluída gera commit atômico próprio, publicado e verificado antes da próxima escrita no mesmo repositório.
- Commits publicados não são squashados ou reescritos.
- Mudança comportamental exige TDD no seam público.
- Revisão interna pré-commit ocorre nos eixos Spec/Charter e Engineering; aceite pertence ao orquestrador externo.
- Mirrors upstream serão separados e somente leitura.
- Catálogo de API deve ser machine-readable e medir cobertura real.
- Toda mutação MCP declara escopo, risco, idempotência, paginação, versão/edição e auditoria.
- Evidência é proporcional ao risco; plausibilidade não é prova.

## Próximas decisões técnicas esperadas

- fonte de verdade de releases do Runner;
- obtenção/verificação de helper images;
- formato do catálogo de API;
- linguagem/runtime do MCP;
- geração de tools e residual API;
- ambiente isolado de contract tests.
