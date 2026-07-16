# Baseline verificável do pacote GitLab YunoHost

Round-ID: RND-20260716-003
Charter: CHR-WP01-001
Snapshot: master em e2d79f37aeeb765c53c9474f1ea6da3b8ac238b8
Data da inspeção: 2026-07-16
Estado: EXECUTED_AWAITING_REVIEW

## Resultado executivo

O pacote é funcionalmente o mesmo pacote de YunoHost-Apps/gitlab_ynh no
snapshot auditado. A divergência local desta fork é documental: a estrutura
MAESTRO, a continuidade e as especificações foram adicionadas, mas nenhum
manifest, script, template, workflow ou configuração funcional foi alterado.

O baseline instala GitLab Omnibus CE ou EE, versão declarada
19.1.0~ynh1, para amd64 e arm64. A instalação usa a fonte latest correspondente
à edição e à distribuição Debian detectada; upgrades percorrem fontes
intermediárias presentes no manifest. A matriz é grande e fixada por URL e
SHA256, mas o processo que a gera ainda não possui testes automatizados,
dependências pinadas nem uma validação de saída suficientemente forte.

## Identidade e contrato de empacotamento

| Campo | Fato observado | Evidência |
|---|---|---|
| ID e formato | gitlab, packaging format 2 | manifest.toml:1-8 |
| Versão declarada | 19.1.0~ynh1 | manifest.toml:8 |
| YunoHost/helpers | YunoHost >= 12.0.9; helpers 2.1 | manifest.toml:20-23 |
| Arquiteturas | amd64, arm64 | manifest.toml:20-24 |
| Instância | multi_instance=false | manifest.toml:20-24 |
| Edições | Community e Enterprise | manifest.toml:41-48 |
| Recursos | LDAP ativo, SSO false, 500M de disco, 3000M build e 2000M runtime | manifest.toml:26-31 |
| Portas | Nginx 8080, Puma 8081, Sidekiq 8082, Pages 8083 e Nginx Pages 8084 | manifest.toml:89-99 |
| Dependência APT explícita | openssh-server | manifest.toml:101-102 |

O pacote não é um fork do código do produto GitLab. Ele instala os pacotes
Omnibus publicados em packages.gitlab.com e sobrepõe configuração YunoHost em
conf/gitlab.rb, conf/nginx.conf e conf/nginx-pages.conf.

## Matriz de fontes

O manifest contém 52 seções em resources.sources e 104 registros de assets:

| Grupo | Versões | Distribuições | Edições | Arquiteturas | Registros |
|---|---:|---|---|---|---:|
| latest | 19.1.0 | bullseye, bookworm, trixie | CE, EE | amd64, arm64 | 12 |
| Caminho histórico completo | 18.11.5, 18.8.10, 18.5.7 | bullseye, bookworm, trixie | CE, EE | amd64, arm64 | 36 |
| Caminho histórico sem trixie | 18.2.8, 17.11.7, 17.8.7, 17.5.5, 17.3.7, 17.1.8, 16.11.10 | bullseye, bookworm | CE, EE | amd64, arm64 | 56 |

Todos os hashes presentes têm 64 caracteres hexadecimais e todas as URLs
passam pela forma versionada do repositório oficial de pacotes. A inspeção
estrutural não encontrou registro incompleto. Foi feita requisição HEAD para
os 12 assets latest e 4 assets históricos representativos; todos retornaram
HTTP 200. A integridade criptográfica de cada arquivo não foi recalculada
porque a auditoria não baixou os 104 pacotes.

O template em manifest.toml.j2 gera latest e o caminho histórico a partir de
listas de distribuições, arquiteturas e hashes. O código gerador limita as
arquiteturas a amd64/arm64 em upgrade-path.py:36-38, portanto a matriz do
gerador está coerente com o manifest atual, mas isso é uma invariável implícita
e ainda não um teste.

## Arquivos e responsabilidades

| Área | Arquivos | Responsabilidade |
|---|---|---|
| Entrada do pacote | manifest.toml, config_panel.toml, tests.toml | contrato YunoHost, perguntas e cenários de package_check |
| Geração | manifest.toml.j2, upgrade-path.py | descobrir caminho, consultar índices, renderizar fontes e atualizar gitlab.rb |
| Instalação | scripts/install, scripts/_common.sh | parâmetros, Pages, swap, sysctl, pacote, usuário, serviço e Nginx |
| Upgrade | scripts/upgrade | compatibilidade mínima, caminho intermediário, migrações, reconfigure e serviço |
| Backup/restore | scripts/backup, scripts/restore | backup Omnibus, configuração, banco, restauração e check |
| Configuração | scripts/config, scripts/change_url | Pages, URL, permissões, Nginx e reconfigure |
| Remoção | scripts/remove | serviço, pacote, configuração, dados e swap |
| Runtime | conf/gitlab.rb, conf/nginx.conf, conf/nginx-pages.conf | defaults Omnibus e proxy YunoHost |
| CI | .gitlab-ci.yml, .github/workflows/updater.yml, .github/workflows/updater.sh | linter, atualização agendada e criação de PR |

Não há suíte de testes Python ou shell no repositório. tests.toml declara
cenários de instalação, upgrade, Pages e Enterprise para o package_check.

## Mapa de lifecycle observado

### Install

scripts/install armazena defaults, valida Pages e domínio dedicado, calcula
swap para hosts com menos de 4 GiB, tenta aplicar parâmetros de kernel, gera
gitlab.rb, instala a fonte latest da edição e distribuição detectadas, cria o
administrador GitLab, registra o serviço gitlab-runsvdir, recarrega Nginx e
aguarda Puma. Evidência principal: scripts/install:7-173.

### Upgrade

scripts/upgrade recusa origem abaixo de 16.9.0~ynh1, garante defaults,
prepara swap e kernel, lê a versão instalada, escolhe a próxima fonte no
manifest e repete a instalação até chegar à latest. Entre etapas, espera
batched background migrations; depois reconfigura GitLab, Nginx e Pages.
Evidência principal: scripts/upgrade:7-223 e scripts/upgrade:225-321.

O caminho efetivo é limitado ao que foi materializado em
resources.sources. Quando a versão seguinte não existe no mesmo major, o
script tenta o primeiro ponto do major seguinte e depois cai em latest.
Isso precisa de testes de contrato contra a matriz oficial antes de ser
tratado como prova de cobertura completa.

### Backup

scripts/backup salva a configuração Nginx principal, a configuração Pages
quando habilitada, o backup Omnibus last_gitlab_backup.tar, gitlab-secrets.json,
gitlab.rb e gitlab-persistent.rb. O backup de dados depende do mecanismo
gitlab-backup do pacote. Evidência: scripts/backup:11-52.

### Restore

scripts/restore restaura Nginx e configuração, reinstala a fonte latest da
edição/distribuição atual, restaura o backup Omnibus, executa
gitlab-backup restore, corrige o ownership do registry quando aplicável,
recria o serviço, reinicia GitLab, executa gitlab:rake gitlab:check SANITIZE=true
e restaura Pages. Evidência: scripts/restore:11-139.

O restore não seleciona explicitamente o mesmo build que originou o backup:
ele usa a fonte latest disponível no manifest. Compatibilidade entre o
backup e esse build é uma hipótese operacional ainda não demonstrada neste
baseline.

### Change URL e configuração

scripts/change_url reaplica Nginx, parâmetros de kernel e gitlab.rb com o novo
domínio/path, reconfigura e reinicia GitLab. scripts/config permite alterar
use_web_account, Pages e pages_url, atualiza permissões e move a configuração
Nginx quando o domínio Pages muda. Evidências: scripts/change_url:7-61 e
scripts/config:19-114.

### Remove

scripts/remove remove o serviço YunoHost, para GitLab, remove o pacote CE ou
EE, apaga configuração, Nginx, dados em /var/opt/gitlab e o swap criado pelo
aplicativo. Evidência: scripts/remove:7-71. A operação é destrutiva e não foi
executada nesta auditoria.

## Verificações realizadas

| Verificação | Resultado |
|---|---|
| Parsing TOML de manifest, config_panel e tests | VERIFIED |
| bash -n em todos os scripts e updater.sh | VERIFIED |
| py_compile de upgrade-path.py | VERIFIED; cache transitório removido |
| Forma dos 104 hashes e URLs | VERIFIED estruturalmente |
| HEAD de 16 assets GitLab representativos | VERIFIED, HTTP 200 |
| upgrade-path.json oficial | VERIFIED como acessível; retornou 35 versões e alvo final 19.1.2 no momento da auditoria |
| Package linter | UNVERIFIED: o ambiente não possui jsonschema |
| Execução YunoHost install/upgrade/backup/restore | UNVERIFIED: não há host YunoHost neste ambiente |
| Execução do gerador | UNVERIFIED: jinja2 não está instalado e o gerador não tem modo dry-run |

## Limitações

O snapshot foi auditado fora de um host YunoHost e sem baixar todos os
pacotes. Os resultados sobre serviço, permissões, PostgreSQL, LDAP, Pages,
reconfigure, migrações e restore permanecem observados por leitura estática,
não demonstrados em runtime.
