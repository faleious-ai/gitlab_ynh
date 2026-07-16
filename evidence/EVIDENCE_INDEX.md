# Índice de evidências

## Estados

`OBSERVED`, `VERIFIED`, `FAILED`, `UNVERIFIED`, `SUPERSEDED`.

## Evidências do programa

| ID | Estado | Round | Assunto | Resultado |
|---|---|---|---|---|
| EVD-20260716-001 | VERIFIED | RND-20260716-001 | bootstrap MAESTRO | estrutura criada sem mudança funcional |
| EVD-20260716-002 | VERIFIED | RND-20260716-002 | orquestração/Codex | papéis, charter, revisão e persistência remota definidos |
| EVD-WP01-GITLAB-INVENTORY | VERIFIED | RND-20260716-003 | baseline GitLab | inventário e limitações documentados |
| EVD-WP01-RUNNER-INVENTORY | VERIFIED | RND-20260716-003 | baseline Runner | sources, helper, Docker, tokens, action e lifecycle documentados |
| EVD-WP01-ORCHESTRATOR-REVIEW | VERIFIED | RND-20260716-004 | revisão WP-01 | verdict `ACCEPTED` |
| EVD-WP02-ORCHESTRATOR-REVIEW-005 | VERIFIED | RND-20260716-006 | revisão fundação WP-02 | verdict `CORRECTION_REQUIRED` |
| EVD-WP02C-LIVE-DISCOVERY | OBSERVED | RND-20260716-007 | descoberta online | API paginada e stable-only; self-link/page ainda não demonstrado |
| EVD-WP02C-CHECKSUM-TRUST | FAILED | RND-20260716-007 | checksum/signature | hashes confrontados, mas falha criptográfica pode ser rebaixada |
| EVD-WP02C-MANIFEST-CANDIDATE | VERIFIED | RND-20260716-007 | manifest candidato | cópia completa, nove campos allowlisted e sem promoção |
| EVD-WP02C-TOKEN-NOT-IN-ARGV | OBSERVED | RND-20260716-007 | registro seguro | subprocesso principal usa ambiente; interface legada permanece |
| EVD-WP02C-YUNOHOST-ACTION | FAILED | RND-20260716-007 | config panel | botão sem controlador `run__register()` e sem entradas efêmeras |
| EVD-WP02C-LIFECYCLE | FAILED | RND-20260716-007 | backup/restore | identidade não preservada; restore depende de senha não persistida |
| EVD-WP02C-TESTS-CI | UNVERIFIED | RND-20260716-007 | testes/CI | testes locais declarados; sem run/status remoto |
| EVD-WP02C-CROSS-REPO-SYNTHESIS | VERIFIED | RND-20260716-007 | síntese | commits e continuidade reconciliados |
| EVD-WP02C-ORCHESTRATOR-REVIEW | VERIFIED | RND-20260716-008 | revisão independente | `continuity/reviews/REV-RND-20260716-007.md`; verdict `CORRECTION_REQUIRED` |

## Evidências requeridas para CHR-WP02-003

- `EVD-WP02D-YUNOHOST-RUN-CONTROLLER`;
- `EVD-WP02D-EPHEMERAL-REGISTRATION-INPUTS`;
- `EVD-WP02D-LIFECYCLE-IDENTITY`;
- `EVD-WP02D-SIGNATURE-FAIL-CLOSED`;
- `EVD-WP02D-SELF-LINK-REDIRECTS`;
- `EVD-WP02D-CANONICAL-EVIDENCE`;
- `EVD-WP02D-LOCAL-TESTS`;
- `EVD-WP02D-REMOTE-CI`;
- `EVD-WP02D-CROSS-REPO-SYNTHESIS`;
- `EVD-WP02D-ORCHESTRATOR-REVIEW`.

## Convenção

O Runner é a fonte funcional. Claims sem prova permanecem `OBSERVED` ou `UNVERIFIED`. Fixture não é autoridade de freshness ou checksum por si só. Nunca reproduzir a credencial histórica.