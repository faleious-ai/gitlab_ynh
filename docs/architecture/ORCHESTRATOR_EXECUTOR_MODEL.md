# Modelo Orquestrador–Executor v2

## Maestro Diretor

Define missão, prioridade, consequência prática, risco aceito, custo, privilégio e irreversibilidade.

## ChatGPT Orquestrador/Revisor

Mantém mandato, backlog, acceptance tests e decisões. Escreve o oracle do objetivo, revisa receipts/commits e registra `accepted`, `correction_required`, gate ou rejeição. Não executa produção em nome do usuário.

## Codex Executor

Atualiza os dois repositórios por fast-forward, executa `doctor`, consome o planner, abre lanes reais, usa TDD, integra serialmente, prepara receipts, publica um commit por tarefa e continua até stop/checkpoint válido. Não altera oracles, não edita tarefa para “completed” e não se aceita.

## Subagentes

Produzem artifacts e logs em snapshots isolados. Workers distintos e overlap são verificados. Não fazem commit/push nem editam memória canônica.

## Revisão pendente

`task_remote_verified` satisfaz dependências técnicas reversíveis. Release, deploy, promoção, credenciais e destruição continuam bloqueados até aceite/gate apropriado.
