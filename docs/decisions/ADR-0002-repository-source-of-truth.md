# ADR-0002 — Repositório como fonte de verdade

Status: `ACCEPTED`  
Data: 2026-07-16

## Contexto

Chats, modelos e sessões são transitórios. Um agente novo não deve inferir decisões, progresso ou contratos a partir de memória conversacional incompleta.

## Decisão

A autoridade é distribuída por camadas persistidas:

- `CONTEXT.md`: propósito e restrições estáveis;
- especificações: contrato do que deve ser construído;
- ADRs: rationale durável;
- `STATUS.md`: fatos atuais;
- `HANDOFF_CURRENT.md`: próximo ponto de retomada;
- `EXECUTION_PLAN.md`: ordem e dependências;
- `EVIDENCE_INDEX.md`: provas;
- registros de rodada e Git: proveniência.

O chat é instrumento de execução, nunca registro canônico.

## Consequências

- Toda descoberta relevante precisa ser promovida ao arquivo correto.
- Agentes devem carregar contexto sob demanda, evitando tanto cegueira quanto excesso de contexto.
- Contradição entre chat e repositório é resolvida em favor do repositório, salvo correção humana explícita persistida.
- Documentos obsoletos devem ser marcados como superseded, não silenciosamente tratados como vigentes.