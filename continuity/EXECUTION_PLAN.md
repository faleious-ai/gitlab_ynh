# Plano de execução — visão humana v2

A autoridade executável é `continuity/PROGRAM_BACKLOG.json`; status, tasks dinâmicas, elegibilidade, lanes, checkpoints e conclusão são calculados pelo motor. Este arquivo descreve apenas a sequência macro.

1. WP-00/WP-01 — governança, baseline e arquitetura v2 endurecida: aceitos.
2. WP-02 Runner — suíte/CI, candidato live Runner/helper images, lifecycle Linux e automação sem promoção.
3. WP-03 GitLab — catálogo live, upgrade graph, candidato fixado e lifecycle.
4. WP-04 — preparação de mirrors; criação externa permanece gated.
5. WP-05/WP-06 — núcleo MCP real, catálogos REST/GraphQL e availability matrix.
6. WP-07 — ondas read, collaboration, repository, CI/CD, releases e admin policy.
7. WP-08 — contract assurance e coverage gate.
8. WP-09 — release/promoção gated e manutenção recorrente.

O Executor pode atravessar work packages quando o planner libera dependências reversíveis. Correções dinâmicas de findings entram no mesmo índice canônico. Paralelismo substantivo usa workers e workspaces isolados; integração e publicação permanecem seriais por task.
