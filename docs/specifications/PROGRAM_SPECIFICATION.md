# Especificação canônica do programa GitLab/Runner/MCP

Status: `ACTIVE_PROGRAM_V2`
Issue dashboard: `faleious-ai/gitlab_ynh#1`
Autoridade machine-readable: `continuity/PROGRAM_BACKLOG.json`

## Missão

Entregar e manter:

1. pacotes YunoHost do GitLab e GitLab Runner atualizáveis por automação reproduzível;
2. versões, URLs, assets e SHA-256 fixados, com upgrade paths obrigatórios;
3. mirrors upstream somente leitura e auditáveis;
4. MCP GitLab version/edition-aware com cobertura REST/GraphQL mensurável;
5. policy gates, redaction, traceability e contract assurance;
6. continuidade operacional independente do chat.

## Objetivos T1–T8

Os objetivos da issue coordenadora são identificados como `T1` a `T8` no backlog. Cada objetivo deve mapear para pelo menos um work package e cada work package para tarefas concretas. `doctor` falha quando a cobertura está incompleta.

## Restrições permanentes

- `master` exclusiva, sem branch/PR/worktree/force push;
- um commit por tarefa e por repositório afetado;
- nenhum `latest` resolvido em instalação;
- sem promoção, release, deploy, credencial real ou operação destrutiva sem gate;
- Runner e helper images são conjunto atômico;
- MCP não declara cobertura sem endpoint/operação, escopo, risco e teste;
- fixture, busca textual e estrutura não provam comportamento live.

## Definition of Done

O programa só fica completo quando todos os tasks do backlog estão `accepted` ou `superseded`, os gates residuais estão fechados, os dois pacotes possuem updater/lifecycle demonstrados, mirrors operam, MCP e coverage gate estão entregues, assurance está verde no nível exigido e a manutenção recorrente é executável pelo mesmo motor.
