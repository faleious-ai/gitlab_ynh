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

## Evidências de RND-20260716-009

| ID | Estado | Task | Assunto | Resultado |
|---|---|---|---|---|
| EVD-PROC-ADR006 | LOCAL_VERIFIED | T-01 | commits por tarefa e decisões D1–D5 | ADR/protocolos publicados cross-repo |
| EVD-PROC-CAVEKIT-RESEARCH | LOCAL_VERIFIED | T-02 | análise skill por skill | `docs/research/CAVEKIT_TO_MAESTRO_ADAPTATION.md` |
| EVD-PROC-SKILL-SUITE | STRUCTURALLY_OBSERVED | T-03..T-14 | skills locais no Runner | 12 skills publicadas individualmente; eficácia será avaliada na próxima execução |
| EVD-PROC-LEARNING-LEDGER | LOCAL_VERIFIED | T-15 | memória de aprendizagem | ledger append-only publicado no Runner |
| EVD-PROC-ARCHITECTURE | LOCAL_VERIFIED | T-16 | MAESTRO por tarefa | máquina de estados e papéis reconciliados nos dois repositórios |
| EVD-PROC-CHR003-MIGRATION | LOCAL_VERIFIED | T-17 | charter executável | oito Task-IDs com seams, TDD, gates e dependências |

## Evidências requeridas para CHR-WP02-003

- controlador YunoHost e inputs efêmeros;
- ausência de entry point legado/token em argv;
- lifecycle/identidade;
- assinatura fail-closed;
- self-link/redirects;
- evidência canônica/portátil;
- testes locais;
- CI remoto;
- síntese cross-repo;
- revisão externa.

## Convenção

O Runner é a fonte funcional. Claims sem prova permanecem estruturais ou unverified. Fixture não prova freshness. Busca textual não prova runtime. Nunca reproduzir a credencial histórica. Aceite pertence ao orquestrador.
