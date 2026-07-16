# Baseline cross-repo GitLab e GitLab Runner

Round-ID: RND-20260716-003
Charter: CHR-WP01-001
Data: 2026-07-16

## Snapshots reconciliados

| Repositório | HEAD de master | Upstream comparado | Resultado |
|---|---|---|---|
| faleious-ai/gitlab_ynh | e2d79f37aeeb765c53c9474f1ea6da3b8ac238b8 | YunoHost-Apps/gitlab_ynh b0a6918705efd0c018e7ede7a77cb57021da8f0c | funcionalmente igual; fork acrescenta governança/documentação |
| faleious-ai/gitlab-runner_ynh | 00db3a0d455db06f54305fef13d6ea596ad6967e | YunoHost-Apps/gitlab-runner_ynh a4ac5b53a5c15546acde60d45616a7ecdb92cd3a | funcionalmente igual; fork acrescenta governança/documentação |

Ambos os remotos auditados expõem somente master. Nenhum tag ou branch de
release foi publicado nas forks no snapshot.

## Comparação técnica

| Dimensão | GitLab | GitLab Runner |
|---|---|---|
| Versão baseline | 19.1.0~ynh1 | 18.6.2~ynh1 |
| Arquiteturas | amd64, arm64 | amd64, arm64, armhf |
| Unidade de atualização | pacote CE/EE por Debian e arquitetura | binário Runner mais helper images |
| Fonte | packages.gitlab.com, índices APT, path.json e template Omnibus | S3 gitlab-runner-downloads |
| Updater | workflow agendado + upgrade-path.py | nenhum workflow/updater ativo; bloco autoupdate comentado |
| Executor | GitLab Omnibus, Nginx, Puma, Sidekiq, Pages, PostgreSQL/Redis internos | Docker CE e executor docker |
| Testes declarados | package_check com Pages/Enterprise/upgrade | package_check com token fixture e upgrade |
| Principal risco | caminho obrigatório, geração de gitlab.rb e governança do updater | token exposto, helper atômico, Docker privilegiado e ação ausente |

## Relação operacional

O Runner é um pacote independente. O GitLab pode funcionar sem um Runner
local, enquanto pipelines do GitLab que dependem de execução precisam de um
Runner registrado. Não há código compartilhado entre os repositórios; a
coordenação necessária é de versões, lifecycle, segurança e evidências.

O conjunto de fontes do Runner deve permanecer atômico: o pacote principal e
helper images precisam corresponder à mesma release. No GitLab, CE/EE,
distribuição e arquitetura precisam ser resolvidos como matriz, e o caminho
obrigatório de upgrade não pode ser saltado.

## Achados cross-repo

1. A política master-only da fork é incompatível com o workflow herdado do
   GitLab, que usa testing/branch/PR; o Runner nem sequer possui workflow
   equivalente. A próxima unidade deve resolver a governança de atualização
   para os dois, não apenas trocar URLs.
2. Os dois manifests estão fixados por URL e SHA256, mas ambos dependem de
   automação upstream não versionada ou incompleta para atualizar esses
   campos.
3. O GitLab tem cobertura estrutural mais ampla e lifecycle complexo; o
   Runner tem menor código, mas uma superfície de privilégio maior por Docker
   e tokens.
4. O Runner contém em tests.toml:21 um literal com aparência de token. O valor
   não foi usado, copiado para documentação ou reproduzido neste relatório.
   A ocorrência pública exige limpeza e rotação se ainda puder ser válida.
5. O GitLab não apresentou literal equivalente na varredura atual.

## Backlog integrado

| Ordem | Unidade | Repositório | Dependência crítica | Aceite |
|---:|---|---|---|---|
| 1 | WP-02A/B — fonte e resolver Runner/helper | Runner | resolver versão/arquitetura e destino oficial | conjunto atômico, hashes e falha fechada |
| 2 | WP-02C/D — gerador e lifecycle Runner | Runner | WP-02A/B | diff determinístico, testes negativos e job Docker controlado |
| 3 | WP-03A/B — fonte e grafo GitLab | GitLab | baseline desta rodada | stops oficiais e fixtures |
| 4 | WP-03C/D — matriz CE/EE e manifest | GitLab | WP-03A/B | todas as células e hashes |
| 5 | WP-03E — lifecycle GitLab | GitLab | WP-03D | install/upgrade/restore/Pages demonstrados |
| 6 | WP-04/05+ — mirrors e MCP | programa | gates de ambiente e decisão humana quando aplicável | escopo próprio, fora desta rodada |

## Limitações cross-repo

Os testes de runtime, os tokens de registro, o Docker daemon e o host YunoHost
não estavam disponíveis. Não houve criação de mirror, registro de Runner,
alteração de release ou operação destrutiva.
