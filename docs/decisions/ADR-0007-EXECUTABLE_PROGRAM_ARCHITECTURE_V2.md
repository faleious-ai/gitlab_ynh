# ADR-0007 — Backlog integral, receipts e stop semântico

Status: `ACCEPTED`
Data: 2026-07-17
Autoridade: Maestro Diretor + Orquestrador

## Contexto

A primeira implementação do planner autorizava parada quando a queue manual não continha tasks e aceitava paralelismo apenas por timestamps. Estado de conclusão podia ser editado diretamente e a proteção de oracles dependia de paths informados pelo Executor.

## Decisão

- backlog integral é autoridade; queue é derivada e hash-bound;
- conclusão técnica deriva de receipt SELF publicado no commit da tarefa;
- state contém decisões/gates, não conclusão manual;
- stop distingue programa completo, gate humano e checkpoint;
- findings acionáveis exigem tarefa corretiva;
- proteção usa diff Git real e inventário SHA-256;
- conflitos de path são prefix-aware;
- paralelismo exige journal hash-chained, workers distintos, overlap, artifact e log hashados.

## Consequência

O prompt do Executor passa a exigir `doctor → refresh-queue → plan` e receipts. Nenhuma queue vazia ou relato Markdown pode, isoladamente, encerrar o programa.
