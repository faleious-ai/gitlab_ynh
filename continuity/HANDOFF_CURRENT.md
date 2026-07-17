# Handoff atual

Estado: `READY_FOR_CODEX_FULL_ROUND`  
Charter ativo: `CHR-WP02-004`  
Revisão anterior: `REV-RND-20260716-010 — CORRECTION_REQUIRED`  
Branch: `master`

## Prompt

```text
Leia AGENTS.md e continue.
```

## Retomada

1. Reconciliar `origin/master` deste coordenador e do Runner.
2. Confirmar `CHR-WP02-004 READY` nos dois repositórios.
3. Ler o contrato detalhado no Runner.
4. Atribuir novo `Round-ID` e executar T01–T07.
5. Publicar o commit Runner de continuidade antes do commit correspondente neste coordenador.

## Direção

Resolver exclusivamente:

- entrega/redirect da chave oficial;
- nova observação live pelo commit corrigido;
- reparação de evidência histórica sem promoção retrospectiva;
- default Docker consistente;
- CI honesto e continuidade com SHAs publicados.

Preservar controller, credencial fora do argv, remoção legada, backup/restore sem re-registro, fail-closed, self-link/assets, diff allowlist e ausência de promoção.

## Gate

`HG-RUN-SEC-01` permanece risco histórico externo, não bloqueante. Nenhuma decisão humana está pendente.
