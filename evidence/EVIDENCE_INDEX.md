# Índice de evidências

## Regras

- Evidência deve ser reproduzível ou claramente marcada como observação.
- Claim sem prova recebe estado `UNVERIFIED`.
- Logs com segredos devem ser redigidos antes da persistência.
- Arquivos grandes e artifacts devem ser referenciados, não copiados indiscriminadamente.
- Cada rodada adiciona ou atualiza entradas relacionadas ao seu escopo.

## Estados

- `OBSERVED`: fato inspecionado, ainda sem teste executável.
- `VERIFIED`: demonstrado por teste/check reproduzível.
- `FAILED`: teste executado e falhou.
- `UNVERIFIED`: alegação ou dependência ainda não demonstrada.
- `SUPERSEDED`: evidência substituída.

## Evidências

| ID | Estado | Round | Assunto | Localização | Resultado |
|---|---|---|---|---|---|
| EVD-20260716-001 | VERIFIED | RND-20260716-001 | bootstrap MAESTRO | `AGENTS.md`, `CONTEXT.md`, `continuity/`, `docs/`, `evidence/` | estrutura criada; sem mudança de comportamento |
| EVD-BASELINE-001 | OBSERVED | pre-bootstrap | versão GitLab YNH | `manifest.toml` | baseline observado `19.1.0~ynh1`; auditoria completa pendente |
| EVD-BASELINE-002 | OBSERVED | pre-bootstrap | versão Runner YNH | repositório relacionado `manifest.toml` | baseline observado `18.6.2~ynh1`; auditoria completa pendente |
| EVD-BASELINE-003 | OBSERVED | pre-bootstrap | gaps de autoupdate Runner | repositório relacionado `manifest.toml` | bloco comentado e helper images sem estratégia; validação detalhada pendente |

## Próximas evidências requeridas

- `EVD-WP01-GITLAB-INVENTORY`;
- `EVD-WP01-RUNNER-INVENTORY`;
- `EVD-WP01-UPSTREAM-DIVERGENCE`;
- `EVD-WP01-RISK-MAP`.

## Convenção para outputs

Quando necessário, armazenar detalhes em `evidence/<wp>/<arquivo>` e registrar aqui:

- comando ou método;
- ambiente;
- entrada/commit;
- resultado;
- limitações;
- risco residual.