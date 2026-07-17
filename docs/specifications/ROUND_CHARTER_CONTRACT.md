# Contrato de charter e tarefa — arquitetura v2

## Autoridade

`ACTIVE_ROUND.md` autoriza uma janela de execução. O escopo completo e a próxima tarefa vêm do backlog e do planner. O charter não pode reduzir silenciosamente o programa nem transformar queue derivada em autoridade.

## Tarefa

Cada tarefa do backlog declara:

- `Task-ID`, work package e repositórios;
- dependências e prioridade;
- reversibilidade e classe de operação;
- ownership prefix-aware de paths;
- seam/acceptance e evidências esperadas;
- output e rollback.

## Ciclo

1. `doctor` e `refresh-queue`;
2. `plan` e seleção das lanes;
3. challenge quando aplicável;
4. RED→GREEN no seam público;
5. reviews Spec e Engineering;
6. `prepare-receipt` no repositório da tarefa;
7. commit único contendo mudança, prova e receipt;
8. push, fetch e `HEAD == origin/master`;
9. novo `plan`, que deriva `task_remote_verified` pelo receipt publicado;
10. próxima tarefa elegível.

## Fechamento

O Executor pode terminar a invocação somente quando o planner retornar:

- `stop_allowed=true`; ou
- `checkpoint_allowed=true`, registrando claramente que não é conclusão do programa.

`EXECUTED_AWAITING_REVIEW` significa commits remotos e receipts verificáveis, não aceite.
