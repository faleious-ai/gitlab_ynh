# Limites cross-repo v2

## Coordenador `gitlab_ynh`

Autoridade sobre mandato, backlog, state, findings, issue dashboard, pacote GitLab e preparação temporária do MCP.

## `gitlab-runner_ynh`

Autoridade sobre manifest, updater, helper images, registro, Docker, lifecycle, testes e evidências Runner. Consome o plano do coordenador e inclui receipt local no commit de cada tarefa Runner.

## Futuro `gitlab-mcp`

Autoridade sobre servidor, clientes REST/GraphQL, catálogo, tools, policy, auditoria, contract tests e coverage. A migração ocorre por tarefa cross-repo após criação autorizada.

## Mirrors

Somente leitura. Criação/sync real depende de gate externo; pesquisa, harness e política podem avançar antes.

## Receipt cross-repo

Tarefa com múltiplos repositórios exige receipt com mesmo Task-ID em cada repositório. Só é `task_remote_verified` quando todos os commits estão em seus `origin/master`.
