# Rodada ativa

Charter-ID: `CHR-PROGRAM-V2-CONTINUE-001`
Estado: `READY`
Preparado pelo Orquestrador: 2026-07-17
Próximo Round-ID do Executor: `RND-20260717-017`

## Autorização

Executar todas as tarefas técnicas reversíveis elegíveis do backlog, incluindo tarefas corretivas registradas durante o loop. A autorização atravessa work packages; o planner decide a próxima task.

## Gates

Sem release, deploy, promoção, criação de repositório/mirror, credencial real ou destruição sem gate válido. Trabalho preparatório independente continua.

## Fechamento

Encerrar somente conforme `stop_allowed`/`checkpoint_allowed`. Entregar receipts, commits remotos, lanes validadas, findings e plano final. Queue vazia isolada não autoriza fechamento.
