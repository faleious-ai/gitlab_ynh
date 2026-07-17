# Handoff atual v2

Estado: `READY_FOR_EXECUTOR`
Charter: `CHR-PROGRAM-V2-CONTINUE-001`
Próximo Round-ID: `RND-20260717-017`

## Baseline remoto

- coordenador: `dc2f1166b27c0f41958c69906c8df65a9001e762` mais o commit de ativação desta rodada;
- Runner: `7dc24ccb8b539c052966eee4d22820e51e418433`.

## Retomada obrigatória

1. fast-forward coordenador e Runner em `master` sem descartar trabalho local;
2. confirmar árvores limpas e HEADs remotos;
3. executar `refresh-queue`, `doctor` e `plan`;
4. iniciar ao menos duas lanes reais quando o planner exigir;
5. integrar e publicar uma tarefa por vez com receipt SELF;
6. repetir até stop/checkpoint semanticamente válido.

Queue vazia, CI vermelho, primeira falha ou review pendente não equivalem a conclusão.
