# Índice de evidências

## Estados

`STRUCTURALLY_OBSERVED`, `LOCAL_VERIFIED`, `REMOTE_CI_VERIFIED`, `LIFECYCLE_VERIFIED`, `FAILED`, `UNVERIFIED`, `SUPERSEDED`.

## Evidências do programa

| ID | Estado | Round | Assunto | Resultado |
|---|---|---|---|---|
| EVD-20260716-001 | LOCAL_VERIFIED | RND-20260716-001 | bootstrap MAESTRO | estrutura criada sem mudança funcional |
| EVD-20260716-002 | LOCAL_VERIFIED | RND-20260716-002 | orquestração/Codex | papéis, charter, revisão e persistência remota definidos |
| EVD-WP01-GITLAB-INVENTORY | LOCAL_VERIFIED | RND-20260716-003 | baseline GitLab | inventário e limitações documentados |
| EVD-WP01-RUNNER-INVENTORY | LOCAL_VERIFIED | RND-20260716-003 | baseline Runner | sources, helper, Docker, tokens, action e lifecycle documentados |
| EVD-WP01-ORCHESTRATOR-REVIEW | LOCAL_VERIFIED | RND-20260716-004 | revisão WP-01 | verdict `ACCEPTED` |
| EVD-WP02-ORCHESTRATOR-REVIEW-005 | LOCAL_VERIFIED | RND-20260716-006 | revisão fundação WP-02 | verdict `CORRECTION_REQUIRED` |
| EVD-WP02C-LIVE-DISCOVERY | STRUCTURALLY_OBSERVED | RND-20260716-007 | descoberta online | API paginada/stable-only; self-link/page incompletos |
| EVD-WP02C-CHECKSUM-TRUST | FAILED | RND-20260716-007 | checksum/signature | hashes confrontados, mas falha criptográfica pode ser rebaixada |
| EVD-WP02C-MANIFEST-CANDIDATE | LOCAL_VERIFIED | RND-20260716-007 | manifest candidato | cópia completa, nove campos allowlisted e sem promoção |
| EVD-WP02C-TOKEN-NOT-IN-ARGV | STRUCTURALLY_OBSERVED | RND-20260716-007 | registro seguro | subprocesso principal usa ambiente; interface legada permanece |
| EVD-WP02C-YUNOHOST-ACTION | FAILED | RND-20260716-007 | config panel | botão sem controlador real/inputs efêmeros |
| EVD-WP02C-LIFECYCLE | FAILED | RND-20260716-007 | backup/restore | identidade não preservada; restore depende de senha não persistida |
| EVD-WP02C-TESTS-CI | UNVERIFIED | RND-20260716-007 | testes/CI | testes locais declarados; sem run/status remoto |
| EVD-WP02C-CROSS-REPO-SYNTHESIS | LOCAL_VERIFIED | RND-20260716-007 | síntese | commits e continuidade reconciliados |
| EVD-WP02C-ORCHESTRATOR-REVIEW | LOCAL_VERIFIED | RND-20260716-008 | revisão independente | `CORRECTION_REQUIRED` |

## Evolução do processo

| ID | Estado | Round | Assunto | Resultado |
|---|---|---|---|---|
| EVD-PROC-ADR006 | LOCAL_VERIFIED | RND-20260716-009 | commits por tarefa | política cross-repo publicada |
| EVD-PROC-SKILL-SUITE | STRUCTURALLY_OBSERVED | RND-20260716-009 | skills MAESTRO | suíte inicial publicada e exercitada |
| EVD-WP02D-ORCHESTRATOR-REVIEW | LOCAL_VERIFIED | RND-20260717-011 | revisão integrada | `CORRECTION_REQUIRED` |
| EVD-WP02E-INTEGRATION | LOCAL_VERIFIED | RND-20260717-012 | integração Runner | gates locais e manifest inalterado |
| EVD-RND-20260717-015-GITLAB-CATALOG | STRUCTURALLY_OBSERVED | RND-20260717-015 | catálogo GitLab | rotas oficiais observadas sem promoção |
| EVD-RND-20260717-015-MCP-API-INVENTORY | STRUCTURALLY_OBSERVED | RND-20260717-015 | inventário REST/GraphQL | superfície inicial catalogada |
| EVD-RND-20260717-015-ASSURANCE | LOCAL_VERIFIED | RND-20260717-015 | assurance | acceptance 17/17; limitações preservadas |
| EVD-RND-20260717-015-FINAL-CONTINUITY | LOCAL_VERIFIED | RND-20260717-015 | pacote de revisão | continuidade cross-repo reconciliada |

## Arquitetura v2

| ID | Estado | Round/Task | Resultado |
|---|---|---|---|
| EVD-ARCH-V2-COORDINATOR | LOCAL_VERIFIED | RND-20260717-016 / T-GOV-ARCHITECTURE-V2 | backlog integral, máquina, receipts, findings, proteção e stop semântico publicados em `dc2f1166b27c0f41958c69906c8df65a9001e762` |
| EVD-ARCH-V2-RUNNER | LOCAL_VERIFIED | RND-20260717-016 / T-RUN-ARCHITECTURE-V2 | consumer, contratos e suíte Runner publicados em `7dc24ccb8b539c052966eee4d22820e51e418433` |
| EVD-ARCH-V2-HARDEN-RUNNER | LOCAL_VERIFIED | RND-20260717-016 / T-GOV-ARCHITECTURE-V2-HARDEN | correction tasks dinâmicas e skills v2 em `dafcac9a26e56d8c3731fae66e9e4cc5f5a0d015` |
| EVD-ARCH-V2-HARDEN-COORDINATOR | LOCAL_VERIFIED | RND-20260717-016 / T-GOV-ARCHITECTURE-V2-HARDEN | workspaces, artifacts, identidade/baseline, hashes protegidos e testes 7/7 em `f2b8dc62801c4a2fbddcd28f0a000890b9b94f6f` |

## Convenção

Claims sem prova permanecem estruturais ou unverified. Fixture não prova freshness. Busca textual não prova runtime. Evidência observada é semanticamente imutável. O Runner é a fonte funcional de sua unidade; o coordenador é a autoridade do programa. Aceite pertence ao Orquestrador.
