# Rodada ativa

Charter-ID: `CHR-WP02-003`  
Estado: `READY`  
Preparado em: 2026-07-16  
Orquestrador: ChatGPT com o Maestro Diretor  
Executor principal: Codex  
Repositório funcional: `faleious-ai/gitlab-runner_ynh`  
Unidade: `WP-02 Correção final — action, trust fail-closed e lifecycle seguro`

## Autorização

`Leia AGENTS.md e continue` autoriza a execução integral do charter detalhado no Runner. Atribua novo `Round-ID`, conclua todo trabalho não bloqueado e use o mesmo identificador nos dois repositórios.

## Revisão anterior

`CHR-WP02-002` recebeu `CORRECTION_REQUIRED`. Registro: `continuity/reviews/REV-RND-20260716-007.md`.

## Objetivo cross-repo

Fechar os pontos ainda não demonstrados no Runner:

- controlador YunoHost `run__register()` e entradas efêmeras;
- remoção da interface legada de registro;
- backup/restore que preservem configuração e identidade sem re-registro;
- verificação de assinatura/chave fail-closed;
- self-link/origem/redirects;
- índice funcional canônico e relatórios portáveis;
- CI remoto verificável ou bloqueio objetivo.

## Execução

O charter normativo completo, DAG, critérios e pacote de revisão estão em `faleious-ai/gitlab-runner_ynh/continuity/ACTIVE_ROUND.md` no mesmo estado `READY`.

Este coordenador deve receber apenas:

- síntese da implementação e riscos;
- estado das evidências e CI;
- status, handoff, active round, evidence index e round record;
- mesmo `Round-ID` do Runner.

## Limites

Não promover candidata, registrar Runner real, usar credencial histórica, criar branch/PR/worktree, usar force push ou executar operação destrutiva.

## Gate

`HG-RUN-SEC-01` permanece `UNRESOLVED_NO_AUTHORITY` e não bloqueia a rodada técnica.

## Saída

Um commit publicado por repositório afetado. O Codex encerra em `EXECUTED_AWAITING_REVIEW` somente após sincronização remota e pacote recuperável; não declara `ACCEPTED`.