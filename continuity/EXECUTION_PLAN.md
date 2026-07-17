# Plano de execução — visão humana v2

A autoridade executável é `PROGRAM_BACKLOG.json`; status e elegibilidade são calculados pelo planner. Este arquivo descreve a sequência macro sem duplicar checklists mutáveis.

1. WP-00/WP-01 — governança e baseline: aceitos; arquitetura v2 em ativação.
2. WP-02 Runner — CI/suíte, candidato live, lifecycle Linux e automação.
3. WP-03 GitLab — catálogo live, upgrade graph, candidato e lifecycle.
4. WP-04 — mirrors, com criação externa gated; preparação técnica continua.
5. WP-05/WP-06 — núcleo MCP, catálogos REST/GraphQL e availability matrix.
6. WP-07 — ondas read, collaboration, repository, CI/CD, releases e admin policy.
7. WP-08 — contract assurance e coverage gate.
8. WP-09 — release/promoção gated e manutenção recorrente.

O Executor pode atravessar work packages quando dependências reversíveis estão `task_remote_verified`; não espera review implícito.
