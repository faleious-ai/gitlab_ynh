# Protocolo de execução contínua v2

## START

1. atualizar coordenador e Runner por fast-forward; árvore suja ou divergente é bloqueio de sincronização;
2. ler `AGENTS.md`, `HANDOFF_CURRENT.md`, `STATUS.md`, `ACTIVE_ROUND.md`;
3. executar `doctor`, `refresh-queue` e `plan` com os dois repo mappings;
4. registrar Round-ID e journal de lanes.

## LOOP

Enquanto houver `eligible_tasks`:

1. iniciar no mínimo duas lanes quando `parallelism_required=true`;
2. preparar outputs em workers/snapshots distintos;
3. validar wave;
4. integrar a primeira tarefa da `integration_order`;
5. observar RED, implementar, GREEN e gates;
6. registrar findings técnicos com tarefa corretiva;
7. executar reviews Spec e Engineering;
8. executar `prepare-receipt`;
9. commit/push/fetch e confirmar remoto;
10. repetir `doctor`, `refresh-queue` e `plan`.

## STOP

- `stop_allowed=true`: programa completo ou gate humano válido exclusivo;
- `checkpoint_allowed=true`: review/ambiente externo; persistir estado e pedir revisão, sem declarar conclusão;
- qualquer outro estado: continuar ou corrigir a arquitetura/fila.
