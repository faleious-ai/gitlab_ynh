# ADR-0005 — Orquestrador humano-ChatGPT e execução Codex

Estado: `ACCEPTED`  
Data: 2026-07-16

## Contexto

O projeto será desenvolvido pelo Codex a partir de instruções mínimas como `Leia AGENTS.md e continue`, enquanto o usuário espera discutir decisões e bloqueios com o ChatGPT. Sem papéis explícitos, o executor pode receber trabalho incompleto, parar cedo, pedir decisões técnicas desnecessárias ou declarar conclusão sem revisão independente.

## Decisão

- O usuário é o Maestro Diretor e decide gates humanos.
- O ChatGPT é o orquestrador e revisor via repositório.
- O Codex é o executor principal das rodadas autorizadas.
- Cada rodada é definida em `continuity/ACTIVE_ROUND.md` como unidade completa, após as perguntas humanas necessárias.
- O Codex executa todas as tarefas não bloqueadas, usa subagentes quando o DAG permitir e só para após conclusão integral ou bloqueio humano válido.
- O Codex encerra como `EXECUTED_AWAITING_REVIEW`; aceite pertence ao orquestrador.
- Após bloqueio, o usuário e o orquestrador resolvem a decisão e liberam nova execução vinculada ao mesmo charter quando aplicável.

## Consequências

Há separação entre especificação, execução e aceite; o prompt de retomada pode permanecer curto; o repositório carrega a continuidade; paralelismo aumenta throughput sem transferir autoridade de integração aos subagentes.

## Alternativas rejeitadas

- Codex definir e aprovar a própria rodada: mistura mandato, execução e revisão.
- Trabalho ponto a ponto por prompts sucessivos: aumenta fragmentação e dependência do chat.
- Paralelismo irrestrito: cria conflitos e resultados difíceis de integrar.
