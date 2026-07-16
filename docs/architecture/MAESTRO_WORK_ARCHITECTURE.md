# Arquitetura MAESTRO local

## Finalidade

Tornar o programa GitLab/Runner/MCP uma superfície de trabalho continuável para humanos e agentes, na qual cada mudança atravessa intenção, contrato, execução, validação, revisão, persistência e aprendizagem sem depender do chat.

## Princípio

O modelo descreve e executa; contratos, testes, gates e revisor decidem promoção. Plausibilidade nunca substitui prova. Autonomia técnica é ampla dentro do mandato e limitada por consequência humana, privilégio, risco e irreversibilidade.

## Camadas

1. intenção — usuário, issue ou incidente;
2. especificação — contratos duráveis em `docs/specifications/`;
3. contexto — `AGENTS.md` e índices de progressive disclosure;
4. tarefa — Task-ID, seam, claims, ownership, gates e rollback;
5. execução — TDD, implementação mínima, subagentes e backprop;
6. validação — gates proporcionais e níveis explícitos de evidência;
7. revisão — challenge pré-build, dois eixos internos e revisor externo;
8. persistência — um commit remoto por tarefa, sem squash;
9. governança — ADRs e gates humanos;
10. memória — status, handoff, rounds, evidence index, learning ledgers e Git.

## Máquina de estados

```text
ROUND_READY
  → TASK_SCOPED
  → PRE_BUILD_REVIEW?
  → RED → GREEN
  → VALIDATING
  → INTERNAL_REVIEW
  → TASK_COMMITTED_LOCAL
  → TASK_REMOTE_VERIFIED
  → next TASK | ROUND_INTEGRATION
  → EXECUTED_AWAITING_REVIEW
  → ACCEPTED | CORRECTION_REQUIRED | HUMAN_GATE | REJECTED_UNSAFE
```

Falha inesperada retorna por backprop ao contrato/teste. Falha de sincronização produz `TASK_REMOTE_SYNC_BLOCKED`. Decisão material produz `BLOCKED_HUMAN`.

## Memória em camadas

| Camada | Autoridade |
|---|---|
| orientação | `AGENTS.md` |
| propósito | `CONTEXT.md` |
| contrato | `docs/specifications/` |
| rationale | `docs/decisions/` e `continuity/DECISIONS.md` |
| autorização/tarefas | `continuity/ACTIVE_ROUND.md` |
| estado | `continuity/STATUS.md` |
| retomada | `continuity/HANDOFF_CURRENT.md` |
| prova | `evidence/EVIDENCE_INDEX.md` |
| histórico | `continuity/rounds/` e commits Git |
| aprendizagem funcional | ledger do repositório funcional responsável |

## Unidade de rastreabilidade

A rodada possui Round-ID e baseline. Cada tarefa possui Task-ID e um commit por repositório afetado. O commit liga:

`Task-ID → claims/invariantes → seam → RED/GREEN → gates → evidência → rollback`.

Subagentes produzem outputs; somente o executor integra, valida, commita e publica.

## Evidência

- `STRUCTURALLY_OBSERVED`;
- `LOCAL_VERIFIED`;
- `REMOTE_CI_VERIFIED`;
- `LIFECYCLE_VERIFIED`;
- `UNVERIFIED`;
- `FAILED`.

Um nível não implica o seguinte. Busca textual nunca prova runtime.

## Cross-repo

O repositório funcional mantém implementação, testes, skills e learning ledger de sua unidade. Este coordenador mantém missão, decisões transversais, estado do programa e síntese. Uma tarefa cross-repo usa o mesmo Round-ID/Task-ID e só fecha quando todos os commits correspondentes estão remotos.

## Reversibilidade

Commit por tarefa é a unidade preferencial de reversão. Dependências são explícitas. Commits publicados não são squashados, reordenados ou reescritos. Operação irreversível continua atrás de gate humano.

## Fechamento

Cada tarefa deixa código e prova coerentes. Cada rodada deixa o programa mais fácil de continuar. Se um agente novo precisar reconstruir intenção, falhas ou prova pelo chat, a rodada não fechou corretamente.
