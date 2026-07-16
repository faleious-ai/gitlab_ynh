# Índice de evidências

## Regras

- Evidência deve ser reproduzível ou marcada como observação.
- Claim sem prova recebe `UNVERIFIED`.
- Logs com segredos devem ser redigidos.
- Cada rodada atualiza entradas do seu escopo.
- Trabalho executado pelo Codex só é aceito após revisão independente do orquestrador.

## Estados

- `OBSERVED`: fato inspecionado, sem teste completo.
- `VERIFIED`: demonstrado por check reproduzível.
- `FAILED`: check executado e falhou.
- `UNVERIFIED`: não demonstrado.
- `SUPERSEDED`: substituído.

## Evidências

| ID | Estado | Round | Assunto | Localização | Resultado |
|---|---|---|---|---|---|
| EVD-20260716-001 | VERIFIED | RND-20260716-001 | bootstrap MAESTRO | `AGENTS.md`, `CONTEXT.md`, `continuity/`, `docs/`, `evidence/` | estrutura criada; sem mudança funcional |
| EVD-20260716-002 | VERIFIED | RND-20260716-002 | contrato orquestrador/Codex e paralelismo | `AGENTS.md`, `ACTIVE_ROUND.md`, protocolos, ADR-0005 e especificações | papéis, charter, revisão, bloqueio e subagentes persistidos; sem mudança funcional |
| EVD-BASELINE-001 | OBSERVED | pre-bootstrap | versão GitLab YNH | `manifest.toml` | baseline `19.1.0~ynh1` |
| EVD-BASELINE-002 | OBSERVED | pre-bootstrap | versão Runner YNH | repositório relacionado `manifest.toml` | baseline `18.6.2~ynh1` |
| EVD-BASELINE-003 | OBSERVED | pre-bootstrap | gaps de autoupdate Runner | repositório relacionado `manifest.toml` | bloco comentado/helper sem estratégia |
| EVD-WP01-GITLAB-INVENTORY | VERIFIED | RND-20260716-003 | inventário GitLab | `docs/audit/GITLAB_PACKAGE_BASELINE.md` | manifest, 52 source sections/104 assets, scripts, config, lifecycle e limitações documentados |
| EVD-WP01-RUNNER-INVENTORY | VERIFIED | RND-20260716-003 | inventário Runner | `docs/audit/CROSS_REPO_BASELINE.md`; relatório no repositório relacionado | sources, helper images, Docker, tokens, action e lifecycle documentados |
| EVD-WP01-UPSTREAM-DIVERGENCE | VERIFIED | RND-20260716-003 | comparação upstream | `docs/audit/UPSTREAM_DIVERGENCE.md` | forks funcionalmente iguais aos snapshots YunoHost-Apps; divergência local documental |
| EVD-WP01-RISK-MAP | VERIFIED | RND-20260716-003 | riscos e backlog | `docs/audit/AUTOUPDATE_GAPS.md`, `docs/audit/LIFECYCLE_AND_RISK_MAP.md` | riscos priorizados, critérios e dependências derivados sem correção funcional |
| EVD-WP01-VALIDATION | VERIFIED | RND-20260716-003 | validação estática e de fontes | relatórios de auditoria | TOML/shell/Python, forma de hashes e HEADs representativos; runtime explicitamente não demonstrado |
| EVD-WP01-ORCHESTRATOR-REVIEW | VERIFIED | RND-20260716-004 | revisão independente de WP-01 | `continuity/reviews/REV-RND-20260716-003.md` | charter atendido; commits atômicos cross-repo; achados críticos reproduzidos; verdict `ACCEPTED` |

## Evidências requeridas para CHR-WP02-001

- `EVD-WP02-SECRET-REMEDIATION`;
- `EVD-WP02-REGISTER-ACTION`;
- `EVD-WP02-RELEASE-PROVENANCE`;
- `EVD-WP02-ATOMIC-RESOLVER`;
- `EVD-WP02-GENERATOR-TESTS`;
- `EVD-WP02-CI-AND-REDACTION`;
- `EVD-WP02-ORCHESTRATOR-REVIEW`.

## Convenção para outputs

Registrar método/comando, ambiente, entrada/commit, resultado, limitações e risco residual em `evidence/<wp>/` quando detalhes forem necessários. Nunca reproduzir o valor credential-like histórico.
