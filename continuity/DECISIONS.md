# Registro de decisões

## Uso

Este arquivo é o índice operacional. Decisões duráveis possuem ADR próprio. Decisões locais de uma rodada ficam no registro da rodada e só são promovidas a ADR quando alteram contrato, arquitetura, autoridade, risco ou continuidade.

## Estados

- `PROPOSED`: ainda não autoriza execução dependente.
- `ACCEPTED`: vigente.
- `SUPERSEDED`: substituída por decisão posterior.
- `REJECTED`: considerada e recusada.

## Decisões vigentes

| ID | Estado | Decisão | Autoridade |
|---|---|---|---|
| ADR-0001 | ACCEPTED | desenvolvimento direto e exclusivo em `master`, com um commit por rodada de IA | usuário |
| ADR-0002 | ACCEPTED | repositório e evidência persistida prevalecem sobre contexto de chat | MAESTRO + usuário |
| ADR-0003 | ACCEPTED | “latest” é descoberta automática de versão elegível com pin de URL/hash, nunca resolução dinâmica em instalação | segurança de supply chain |
| ADR-0004 | ACCEPTED | agentes decidem tecnicamente dentro do mandato; humano decide gates de missão, risco e irreversibilidade | usuário |

## Decisões operacionais derivadas

- `gitlab_ynh` é coordenador temporário até existir `gitlab-mcp`.
- `gitlab-runner_ynh` mantém autoridade local sobre implementação e testes do Runner.
- Mirrors upstream serão repositórios separados e somente leitura.
- Catálogo de API deve ser machine-readable e medir cobertura real.
- Toda mutação MCP declara escopo, risco, idempotência, paginação, disponibilidade por versão/edição e campos de auditoria.
- Evidência é proporcional ao risco; fluência ou plausibilidade não contam como prova.

## Próximas decisões esperadas

Não são gates ainda; devem ser decididas tecnicamente durante WP-01/WP-02 e registradas:

- fonte de verdade de releases do Runner;
- método de obtenção e verificação de helper images;
- formato do catálogo de API;
- linguagem e runtime do MCP;
- estratégia de geração de tools e residual API;
- ambiente isolado de contract tests.