# AGENTS.md — programa GitLab/Runner/MCP

## Missão

Executar o programa canônico até conclusão técnica demonstrada ou dependência humana real. O backlog integral, os receipts remotos, os gates e os acceptance tests governam a execução; chat, queue derivada e relato de progresso não são autoridade.

## Contrato de invocação

`Leia AGENTS.md e continue` significa:

1. atualizar `gitlab_ynh` e `gitlab-runner_ynh` por fast-forward em `master`;
2. executar `refresh-queue`, `doctor` e `plan` com os dois repositórios;
3. consumir todas as tarefas reversíveis elegíveis, inclusive correções criadas por findings;
4. usar paralelismo substantivo quando exigido e integração serial;
5. continuar até `stop_allowed=true` ou `checkpoint_allowed=true` com causa explícita.

Não significa executar apenas a primeira task nem encerrar quando `eligible_tasks=[]` em uma queue stale.

## Entrada mínima

Leia, nesta ordem:

- `continuity/HANDOFF_CURRENT.md`;
- `continuity/STATUS.md`;
- `continuity/ACTIVE_ROUND.md`;
- `continuity/PROGRAM_MANDATE.json`;
- `continuity/PROGRAM_BACKLOG.json`;
- `continuity/PROGRAM_STATE.json`;
- `continuity/PROGRAM_FINDINGS.json`.

Depois execute:

```text
python scripts/maestro_program.py refresh-queue --root . --repo coordinator=. --repo runner=../gitlab-runner_ynh
python scripts/maestro_program.py doctor --root . --repo coordinator=. --repo runner=../gitlab-runner_ynh
python scripts/maestro_program.py plan --root . --repo coordinator=. --repo runner=../gitlab-runner_ynh
```

Se `doctor` falhar, corrija drift técnico ou registre checkpoint seguro; não contorne o motor.

## Papéis

- Maestro Diretor humano: missão, prioridade, consequência, custo, privilégio e irreversibilidade.
- ChatGPT Orquestrador/Revisor: mandato, backlog, acceptance, review, gates e aceite.
- Codex Executor: TDD, lanes, integração, receipts, commits e continuidade. Não altera oracles nem se aceita.
- Subagentes/workers: artifacts e logs em snapshots isolados, sem commit/push/edição canônica.

## Loop obrigatório

Enquanto `eligible_tasks` não estiver vazio:

1. use a `integration_order` do planner;
2. se `parallelism_required=true`, inicie ao menos duas lanes com workers distintos;
3. gere artifacts/logs não vazios e valide a wave;
4. integre uma task, observe RED, implemente e deixe GREEN;
5. em falha inesperada, faça backprop e registre finding/tarefa corretiva;
6. execute reviews Spec e Engineering;
7. valide o diff Git real contra paths protegidos;
8. execute `prepare-receipt` no repo da task;
9. crie exatamente um commit por task/repo, contendo mudança, prova e receipt;
10. push sem force, fetch, confirme `HEAD == origin/master`;
11. rode novamente refresh/doctor/plan.

## Ownership e receipts

Conclusão técnica não é editada em `PROGRAM_STATE.json`. O planner deriva `task_remote_verified` do receipt `continuity/task_receipts/<Task-ID>.json` incluído no mesmo commit da task e publicado no remoto.

## Paralelismo

Timestamps Markdown não bastam. Use `lane-start`, `lane-finish` e `validate-wave`. Workers, overlap, artifact e command log hashados são obrigatórios. Paths são comparados por ancestralidade; `evidence/` conflita com `evidence/mcp/`.

## Findings

Finding acionável precisa de tarefa corretiva. Use `register-finding`; não arquive teste falhando como “limitação” quando houver correção técnica reversível.

## Proibições

Sem branch, PR, worktree, force push, squash de commit publicado, segredo, runtime `latest`, promoção, release, deploy, credencial real ou operação destrutiva sem gate. Acceptance tests e specs protegidos pertencem ao Orquestrador.

## Parada

- `stop_allowed=true`: programa completo ou somente gates humanos válidos.
- `checkpoint_allowed=true`: review/ambiente externo; não é conclusão.
- qualquer outro resultado: continuar ou corrigir backlog/state/findings.

O Executor termina em `EXECUTED_AWAITING_REVIEW` ou checkpoint explícito; somente o Orquestrador registra `ACCEPTED`.
