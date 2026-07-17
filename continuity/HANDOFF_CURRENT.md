# Handoff atual

Estado: `EXECUTED_AWAITING_REVIEW`
Charter ativo: `CHR-WP02-003`  
Revisão anterior: `REV-RND-20260716-007 — CORRECTION_REQUIRED`  
Processo vigente: `ADR-0006`  
Branch: `master`

## Prompt

```text
Leia AGENTS.md e continue.
```

## Resultado persistido

`RND-20260716-010` executou T01–T07 no Runner e T08 nos dois repositórios, com o mesmo Charter-ID e commits remotos por tarefa afetada. O Runner terminou em `221634780ecca490ce86c9a0703a21f5b4c53e95`; este coordenador recebe a síntese T08 neste commit.

Gates finais do Runner: 32 testes locais, secret scan limpo, parsers JSON/TOML, Bash, dry-run e allowlist passam; `manifest.toml` permanece `18.6.2~ynh1`. CI remoto não foi recuperado pelo ambiente disponível e permanece `UNVERIFIED`; lifecycle YunoHost real também não foi observado.

Para revisão, usar `continuity/rounds/RND-20260716-010.md`, `evidence/EVIDENCE_INDEX.md` e o intervalo remoto completo. O executor não declara `ACCEPTED`.

## Direção

Corrigir no Runner:

- controlador YunoHost e entradas efêmeras;
- interface legada de token;
- backup/restore da identidade;
- trust criptográfico fail-closed;
- self-link/redirects;
- evidência portátil;
- CI remoto ou bloqueio objetivo.

## Processo

- TDD RED→GREEN em seam público;
- backprop técnico automático;
- challenge pré-build para alto impacto;
- revisão pré-commit em dois eixos;
- sem squash, branch, PR, worktree ou force push;
- próximo commit somente após sincronização do anterior no mesmo repositório.

## Gate

`HG-RUN-SEC-01` permanece risco histórico externo. Não usar/testar o valor antigo e não interromper trabalho técnico por esse gate.
