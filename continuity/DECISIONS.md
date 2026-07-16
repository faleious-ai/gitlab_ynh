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
| ADR-0001 | ACCEPTED | desenvolvimento direto e exclusivo em `master`, com um commit por rodada futura de IA | usuário |
| ADR-0002 | ACCEPTED | repositório e evidência persistida prevalecem sobre contexto de chat | MAESTRO + usuário |
| ADR-0003 | ACCEPTED | “latest” é descoberta de versão elegível com pin de URL/hash, nunca resolução dinâmica em instalação | supply chain |
| ADR-0004 | ACCEPTED | agentes decidem tecnicamente dentro do mandato; humano decide gates de missão, risco e irreversibilidade | usuário |
| ADR-0005 | ACCEPTED | ChatGPT orquestra/revisa; Codex executa charters completos, usa subagentes e não aceita o próprio trabalho | usuário |

## Decisões operacionais derivadas

- `gitlab_ynh` é coordenador temporário até existir `gitlab-mcp`.
- `gitlab-runner_ynh` mantém autoridade local sobre implementação e testes do Runner.
- A frase `Leia AGENTS.md e continue` autoriza apenas o charter `READY` em `ACTIVE_ROUND.md`.
- O orquestrador elimina perguntas humanas necessárias antes de liberar o charter.
- O Codex conclui todas as tarefas não bloqueadas e continua frentes independentes antes de escalar.
- Subagentes não fazem commit nem integração final.
- O estado de saída do Codex é `EXECUTED_AWAITING_REVIEW` ou `BLOCKED_HUMAN`; aceite pertence ao orquestrador.
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
