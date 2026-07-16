# Índice de evidências

## Regras

- Evidência deve ser reproduzível ou marcada como observação.
- Claim sem prova recebe `UNVERIFIED`.
- Logs com segredos devem ser redigidos.
- Trabalho do Codex só é aceito após revisão independente.

## Estados

`OBSERVED`, `VERIFIED`, `FAILED`, `UNVERIFIED`, `SUPERSEDED`.

## Evidências do programa

| ID | Estado | Round | Assunto | Resultado |
|---|---|---|---|---|
| EVD-20260716-001 | VERIFIED | RND-20260716-001 | bootstrap MAESTRO | estrutura criada sem mudança funcional |
| EVD-20260716-002 | VERIFIED | RND-20260716-002 | orquestração/Codex | papéis, charter, revisão, paralelismo e persistência remota definidos |
| EVD-WP01-GITLAB-INVENTORY | VERIFIED | RND-20260716-003 | baseline GitLab | inventário e limitações documentados |
| EVD-WP01-RUNNER-INVENTORY | VERIFIED | RND-20260716-003 | baseline Runner | sources, helper, Docker, tokens, action e lifecycle documentados |
| EVD-WP01-UPSTREAM-DIVERGENCE | VERIFIED | RND-20260716-003 | upstream | divergência funcional/documental classificada |
| EVD-WP01-ORCHESTRATOR-REVIEW | VERIFIED | RND-20260716-004 | revisão WP-01 | verdict `ACCEPTED` |
| EVD-WP02-CROSS-REPO-SYNTHESIS | VERIFIED | RND-20260716-005 | síntese de execução WP-02 | commits e entregas persistidos; aceite reservado ao revisor |
| EVD-WP02-ORCHESTRATOR-REVIEW | VERIFIED | RND-20260716-006 | revisão independente WP-02 | `continuity/reviews/REV-RND-20260716-005.md`; verdict `CORRECTION_REQUIRED` |

## Classificação da rodada WP-02 revisada

- remediação da árvore/scanner/redaction: `VERIFIED`;
- action/helper/matriz estrutural: `OBSERVED`, com lacunas de contrato e argv;
- provenance/checksums: `FAILED` para o critério do charter;
- generator do manifest: `FAILED` para o critério do charter;
- CI remoto: `UNVERIFIED`.

## Evidências requeridas para CHR-WP02-002

- `EVD-WP02C-LIVE-DISCOVERY`;
- `EVD-WP02C-CHECKSUM-TRUST`;
- `EVD-WP02C-SOURCE-BOUNDARY`;
- `EVD-WP02C-MANIFEST-CANDIDATE`;
- `EVD-WP02C-TOKEN-NOT-IN-ARGV`;
- `EVD-WP02C-YUNOHOST-ACTION-CONTRACT`;
- `EVD-WP02C-TESTS-AND-REMOTE-CI`;
- `EVD-WP02C-CROSS-REPO-SYNTHESIS`;
- `EVD-WP02C-ORCHESTRATOR-REVIEW`.

## Convenção

O coordenador aponta para evidência funcional no Runner e persiste síntese, decisão e continuidade. Fixture não é autoridade de freshness ou checksum por si só. Nunca reproduzir a credencial histórica.
