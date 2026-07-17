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
| EVD-PROC-SKILL-SUITE | STRUCTURALLY_OBSERVED | T-03..T-14 | skills locais no Runner | eficácia exercitada em RND-20260716-010 e retropropagada em RND-20260717-011 |
| EVD-PROC-LEARNING-LEDGER | LOCAL_VERIFIED | T-15 | memória de aprendizagem | ledger append-only publicado no Runner |
| EVD-PROC-ARCHITECTURE | LOCAL_VERIFIED | T-16 | MAESTRO por tarefa | máquina de estados e papéis reconciliados nos dois repositórios |
| EVD-PROC-CHR003-MIGRATION | LOCAL_VERIFIED | T-17 | charter executável | oito Task-IDs com seams, TDD, gates e dependências |

## Evidências de CHR-WP02-003 — revisão final

| ID | Estado | Task/round | Resultado cross-repo |
|---|---|---|---|
| EVD-WP02D-YUNOHOST-RUN-CONTROLLER | LOCAL_VERIFIED | T-WP02D-01 / RND-20260716-010 | Runner `ada6b78ca4db00c1dcacda4eb01736f123f6040b`; controlador e inputs efêmeros, sem host real |
| EVD-WP02D-NO-LEGACY-ARGV | LOCAL_VERIFIED | T-WP02D-02 / RND-20260716-010 | Runner `79fb763c6c2d20f9bb1b76e42a266da1b41e8ad9`; interface legada removida |
| EVD-WP02D-LIFECYCLE-IDENTITY | LOCAL_VERIFIED | T-WP02D-03 / RND-20260716-010 | Runner `2f0185cbf8b630f94d9618c9d7afe56cabc434b3`; harness local, lifecycle real não observado |
| EVD-WP02D-SIGNATURE-FAIL-CLOSED | LOCAL_VERIFIED | T-WP02D-04 / RND-20260716-010 | lógica adversarial local passa; transport live da chave falha na revisão integrada |
| EVD-WP02D-SELF-LINK-REDIRECTS | LOCAL_VERIFIED | T-WP02D-05 / RND-20260716-010 | release/download limitados; redirect oficial da chave não coberto |
| EVD-WP02D-CANONICAL-EVIDENCE | FAILED | T-WP02D-06 / RND-20260716-010 | artefato histórico recebeu `key_validity=valid` sem nova observação |
| EVD-WP02D-LOCAL-TESTS | LOCAL_VERIFIED | T-WP02D-01..07 / RND-20260716-010 | 32 testes e gates locais passaram |
| EVD-WP02D-REMOTE-CI | UNVERIFIED | T-WP02D-07 / RND-20260716-010 | nenhum run/status remoto recuperado |
| EVD-WP02D-CROSS-REPO-SYNTHESIS | FAILED | T-WP02D-08 / RND-20260716-010 | commits existem; continuidade manteve referências pré-publicação |
| EVD-WP02D-ORCHESTRATOR-REVIEW | LOCAL_VERIFIED | RND-20260717-011 | `continuity/reviews/REV-RND-20260716-010.md`; verdict `CORRECTION_REQUIRED`; coordinator review commit `bece03b10d2ba56caa8bea55c1d032f38fcd7a9c` |

## Evidências finais de RND-20260717-012

| ID | Estado | Round/Task | Resultado cross-repo |
|---|---|---|---|
| EVD-WP02E-KEY-TRANSPORT | LOCAL_VERIFIED | T01 / RND-20260717-012 | Runner `6fb500ec3474c07137fcb8962512ed0adc59a9bb`; cadeia capturada e adversários fail-closed |
| EVD-WP02E-LIVE-TRUST | UNVERIFIED | T02 / RND-20260717-012 | `evidence/wp02e-live-trust-observation.json`; falha antes da chave/GPG |
| EVD-WP02E-HISTORICAL-PROVENANCE | LOCAL_VERIFIED | T03 / RND-20260717-012 | Runner `ea9774001fbf181b5fc210a17fad6a1208a83d4c`; hashes pré-T06 e supersessão |
| EVD-WP02E-DOCKER-DEFAULT | LOCAL_VERIFIED | T04 / RND-20260717-012 | Runner `2563fc31e1b71db89315fd8c707235ed98659962`; `alpine:3.20` consistente |
| EVD-WP02E-REMOTE-CI | UNVERIFIED | T05 / RND-20260717-012 | `workflow_runs=[]`, `statuses=[]`, `gh` ausente; gates locais separados |
| EVD-WP02E-INTEGRATION | LOCAL_VERIFIED | T06 / RND-20260717-012 | Runner `08563cbd2c957e6cca16ae6535a56ef9b2d52b9e`; integração local e manifest inalterado |
| EVD-WP02E-FINAL-CONTINUITY | LOCAL_VERIFIED | T07 / RND-20260717-012 | Runner `652c24819bc778eed04fb9eebe4836ab5ad016f2` + este commit; síntese reconciliada |
| EVD-WP02E-PROCESS-BACKPROP | LOCAL_VERIFIED | RND-20260717-011 | Runner `4cefe926732c95344c3d7d129aa9dbe110dcae72` |

## Evidencias de RND-20260717-015

| ID | Estado | Task | Assunto | Resultado |
|---|---|---|---|---|
| EVD-RND-20260717-015-GITLAB-CATALOG | STRUCTURALLY_OBSERVED | T-GITLAB-02-live-catalog | catalogo oficial GitLab CE/EE | rotas Debian/bookworm observadas sem promocao |
| EVD-RND-20260717-015-MCP-API-INVENTORY | STRUCTURALLY_OBSERVED | T-MCP-02-api-inventory | inventario REST/GraphQL oficial | superficie de leitura catalogada; disponibilidade por instancia permanece descoberta |
| EVD-RND-20260717-015-ASSURANCE | LOCAL_VERIFIED | T-ASSURANCE-01-maintenance | gates proporcionais | 17/17 acceptance; Bash/parsing/secret scan/dry-run; limites ambientais e CI falho preservados |

## Convenção

O Runner é a fonte funcional. Claims sem prova permanecem estruturais ou unverified. Fixture não prova freshness. Busca textual não prova runtime. Evidência observada é semanticamente imutável. Nunca reproduzir a credencial histórica. Aceite pertence ao orquestrador.
