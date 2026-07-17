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

## Evidências de CHR-WP02-003 — RND-20260716-010

| ID | Estado | Task/round | Resultado cross-repo |
|---|---|---|---|
| EVD-WP02D-YUNOHOST-RUN-CONTROLLER | LOCAL_VERIFIED | T-WP02D-01 / RND-20260716-010 | Runner `ada6b78ca4db00c1dcacda4eb01736f123f6040b`; controlador e inputs efêmeros verificados localmente, sem host YunoHost real |
| EVD-WP02D-NO-LEGACY-ARGV | LOCAL_VERIFIED | T-WP02D-02 / RND-20260716-010 | Runner `79fb763c6c2d20f9bb1b76e42a266da1b41e8ad9`; interface legada removida, sem token em argv ativo |
| EVD-WP02D-LIFECYCLE-IDENTITY | LOCAL_VERIFIED | T-WP02D-03 / RND-20260716-010 | Runner `2f0185cbf8b630f94d9618c9d7afe56cabc434b3`; harness backup/restore preserva identidade sem re-registro; lifecycle real não observado |
| EVD-WP02D-SIGNATURE-FAIL-CLOSED | LOCAL_VERIFIED | T-WP02D-04 / RND-20260716-010 | Runner `35e8e44dd9fb39b47ad71e6dfb06e854c0029618`; falhas criptográficas adversas fecham; chave/assinatura real não usada |
| EVD-WP02D-SELF-LINK-REDIRECTS | LOCAL_VERIFIED | T-WP02D-05 / RND-20260716-010 | Runner `51dbb98a7e6de477c4f3234b1c7d40b4ac1a54ac`; self-link, paths e redirects limitados verificados em adapters falsos |
| EVD-WP02D-CANONICAL-EVIDENCE | LOCAL_VERIFIED | T-WP02D-06 / RND-20260716-010 | Runner `2acc1a3ec1a6c42a81eacea02f7ae093131070de`; JSONs portáveis, índice task→SHA e validade observada |
| EVD-WP02D-LOCAL-TESTS | LOCAL_VERIFIED | T-WP02D-01..07 / RND-20260716-010 | Runner `2d9cb41f41f292f3b4bd19513b91ca66720457d6`; 32 testes, scanner, parsers, Bash e dry-run finais passaram |
| EVD-WP02D-REMOTE-CI | UNVERIFIED | T-WP02D-07 / RND-20260716-010 | workflow read-only e actions fixadas; run/status remoto do SHA funcional não foi recuperado neste ambiente |
| EVD-WP02D-CROSS-REPO-SYNTHESIS | LOCAL_VERIFIED | T-WP02D-08 / RND-20260716-010 | Runner `221634780ecca490ce86c9a0703a21f5b4c53e95` reconciliado com este coordenador; matriz, manifest e continuidade fechados |
| EVD-WP02D-ORCHESTRATOR-REVIEW | UNVERIFIED | T-WP02D-08 / RND-20260716-010 | revisão independente e aceite pertencem ao ChatGPT; não declarar `ACCEPTED` |

## Convenção

O Runner é a fonte funcional. Claims sem prova permanecem estruturais ou unverified. Fixture não prova freshness. Busca textual não prova runtime. Nunca reproduzir a credencial histórica. Aceite pertence ao orquestrador.
