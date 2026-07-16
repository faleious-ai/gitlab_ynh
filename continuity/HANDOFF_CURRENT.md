# Handoff atual

Estado: `READY_FOR_CODEX_FULL_ROUND`  
Charter ativo: `CHR-WP02-001`  
Revisão anterior: `REV-RND-20260716-003 — ACCEPTED`  
Branch: `master`

## Prompt de retomada

```text
Leia AGENTS.md e continue.
```

## Retomada mínima

1. Ler `AGENTS.md`.
2. Confirmar HEAD de `master` neste repositório e em `faleious-ai/gitlab-runner_ynh`.
3. Ler `continuity/STATUS.md` e `continuity/ACTIVE_ROUND.md`.
4. Confirmar `Charter-ID: CHR-WP02-001` e estado `READY`.
5. Atribuir novo `Round-ID` e executar integralmente o DAG, com o Runner como repositório primário.

## Rodada autorizada

A rodada combina o maior volume coerente de trabalho técnico não bloqueado:

- remover a credencial persistida da árvore atual e impedir recorrência;
- reparar ou remover justificadamente a action `register` sem target;
- centralizar e testar o fluxo de registro sem usar token real;
- implementar fonte, resolver e generator determinístico para Runner + helper images;
- adicionar fixtures offline, testes negativos e CI somente de validação;
- atualizar este coordenador com síntese e evidência.

Não promover versão de produção, não registrar Runner real e não executar ação destrutiva.

## Paralelismo

O charter define frentes independentes para segurança, action/registro, proveniência, resolver/generator e assurance. Subagentes não fazem commit. O Codex integra interfaces, executa validação final e persiste um commit por repositório.

## Gate humano

`HG-RUN-SEC-01` permanece aberto: o valor histórico deve ser revogado, rotacionado ou confirmado como expirado por quem administra o projeto GitLab usado pelo package_check.

O Codex não deve usar ou validar o valor. Esse gate não autoriza interrupção precoce: todas as tarefas técnicas independentes devem ser concluídas primeiro.

## Estado de saída esperado

- `EXECUTED_AWAITING_REVIEW`, se o gate humano estiver resolvido ou não fizer parte do critério técnico final; ou
- `BLOCKED_HUMAN`, somente após todo o restante estar concluído, com ação humana exata registrada.

O Codex entrega commits, evidências, matriz tarefa-output-evidência, testes, riscos e estado do gate. Não marca `ACCEPTED`.
