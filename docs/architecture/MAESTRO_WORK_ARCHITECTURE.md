# Arquitetura MAESTRO de trabalho — v2

## Princípio

O backlog define tudo que existe para fazer; receipts e Git demonstram o que foi entregue; estado do Orquestrador decide aceite e gates; queue é somente uma projeção.

## Camadas

1. missão e limites — `PROGRAM_MANDATE.json`;
2. escopo integral — `PROGRAM_BACKLOG.json`;
3. decisões/gates — `PROGRAM_STATE.json`;
4. findings — `PROGRAM_FINDINGS.json`;
5. projeção — `PROGRAM_QUEUE.json`;
6. execução — planner, lanes, TDD e receipts;
7. prova — commits, evidence index e CI/lifecycle;
8. revisão — Orquestrador;
9. memória — status, handoff, rounds e Git.

## Máquina efetiva

```text
planned/auto-activatable
  → ready (derivado por dependências)
  → lane running
  → RED → GREEN
  → receipt SELF preparado
  → task commit publicado
  → task_remote_verified (derivado)
  → accepted | correction_required (Orquestrador)
```

Bloqueios são `blocked_environment` ou `blocked_human`; somente o segundo pode produzir `stop_allowed=true`, com gate completo e nenhuma tarefa independente.

## Conclusão

`PROGRAM_COMPLETE` exige todos os tasks `accepted`/`superseded`. Review ou ambiente pendente gera checkpoint, nunca conclusão.
