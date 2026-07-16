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
| EVD-WP01-ORCHESTRATOR-REVIEW | VERIFIED | RND-20260716-004 | revisão WP-01 | verdict ACCEPTED |
| EVD-WP02-CROSS-REPO-SYNTHESIS | VERIFIED | RND-20260716-005 | síntese anterior | aceite reservado ao revisor |
| EVD-WP02-ORCHESTRATOR-REVIEW | VERIFIED | RND-20260716-006 | revisão anterior | CORRECTION_REQUIRED |
| EVD-WP02-LIVE-DISCOVERY | VERIFIED | RND-20260716-007 | descoberta online | v19.2.0 pela API oficial paginada |
| EVD-WP02-CHECKSUM-TRUST | VERIFIED | RND-20260716-007 | checksum/signature | quatro hashes confrontados; assinatura verificada |
| EVD-WP02-MANIFEST-CANDIDATE | VERIFIED | RND-20260716-007 | manifest candidate | cópia completa, diff de nove campos, sem promoção |
| EVD-WP02-TOKEN-NOT-IN-ARGV | VERIFIED | RND-20260716-007 | registro seguro | fake sem token em argv/stdout/stderr |
| EVD-WP02-YUNOHOST-ACTION | VERIFIED | RND-20260716-007 | action contract | config_panel.toml + scripts/config |
| EVD-WP02-TESTS-CI | VERIFIED | RND-20260716-007 | testes/CI | 14 testes, scanner, parsing, Bash, workflow_dispatch e SHA pins |
| EVD-WP02-CROSS-REPO-SYNTHESIS-007 | VERIFIED | RND-20260716-007 | síntese cross-repo | estado coordenado EXECUTED_AWAITING_REVIEW |

## Convenção

O Runner é a fonte funcional; este índice persiste a síntese. Fixture não é autoridade de freshness ou checksum por si só. Nunca reproduzir a credencial histórica.
