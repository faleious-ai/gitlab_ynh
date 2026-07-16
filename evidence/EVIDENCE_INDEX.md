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
| EVD-BASELINE-001 | OBSERVED | pre-bootstrap | versão GitLab YNH | `manifest.toml` | baseline `19.1.0~ynh1`; auditoria pendente |
| EVD-BASELINE-002 | OBSERVED | pre-bootstrap | versão Runner YNH | repositório relacionado `manifest.toml` | baseline `18.6.2~ynh1`; auditoria pendente |
| EVD-BASELINE-003 | OBSERVED | pre-bootstrap | gaps de autoupdate Runner | repositório relacionado `manifest.toml` | bloco comentado/helper sem estratégia; detalhamento pendente |
| EVD-WP01-GITLAB-INVENTORY | VERIFIED | RND-20260716-003 | inventário GitLab | `docs/audit/GITLAB_PACKAGE_BASELINE.md` | manifest, 52 source sections/104 assets, scripts, config, lifecycle e limitações documentados |
| EVD-WP01-RUNNER-INVENTORY | VERIFIED | RND-20260716-003 | inventário Runner | `docs/audit/CROSS_REPO_BASELINE.md`; relatório no repositório relacionado | sources, helper images, Docker, tokens, ação e lifecycle documentados |
| EVD-WP01-UPSTREAM-DIVERGENCE | VERIFIED | RND-20260716-003 | comparação upstream | `docs/audit/UPSTREAM_DIVERGENCE.md` | forks funcionalmente iguais aos snapshots YunoHost-Apps; divergência local é documental |
| EVD-WP01-RISK-MAP | VERIFIED | RND-20260716-003 | riscos e backlog | `docs/audit/AUTOUPDATE_GAPS.md`, `docs/audit/LIFECYCLE_AND_RISK_MAP.md` | riscos priorizados, critérios e dependências derivados sem implementar correções |
| EVD-WP01-VALIDATION | VERIFIED | RND-20260716-003 | validação estática e de fontes | relatórios de auditoria | TOML/shell/Python, forma de hashes e HEADs representativos; limites de runtime explicitados |

## Verificação de EVD-20260716-002

- `AGENTS.md` contém semântica de invocação e papéis.
- `continuity/ACTIVE_ROUND.md` contém charter WP-01 completo e DAG paralelo.
- `ROUND_PROTOCOL.md` exige execução de todo trabalho não bloqueado.
- `REVIEW_PROTOCOL.md` separa execução de aceite.
- `PARALLEL_EXECUTION_POLICY.md` restringe ownership e commit de subagentes.
- Nenhum manifest ou script funcional foi modificado.

## Evidências ainda requeridas

- `EVD-WP01-ORCHESTRATOR-REVIEW`.

## Convenção para outputs

Registrar método/comando, ambiente, entrada/commit, resultado, limitações e risco residual em `evidence/<wp>/` quando detalhes forem necessários.
