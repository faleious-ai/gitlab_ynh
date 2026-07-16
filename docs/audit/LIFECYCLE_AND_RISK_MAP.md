# Mapa de lifecycle e riscos — GitLab YunoHost

Round-ID: RND-20260716-003
Estado: baseline auditado estaticamente

## Fluxo operacional

| Evento | Caminho | Pré-condições | Efeitos principais | Evidência |
|---|---|---|---|---|
| Install | scripts/install | domínio/path, edição, admin, Pages | configura swap/kernel, instala CE/EE, cria admin, registra serviço e proxy | scripts/install:7-173 |
| Upgrade | scripts/upgrade | origem >= 16.9.0~ynh1, fontes intermediárias | espera migrações, instala etapas do caminho, reconfigura e reinicia | scripts/upgrade:20-236 |
| Backup | scripts/backup | serviço e gitlab-backup operacionais | salva banco/dados Omnibus, secrets, config, Nginx e Pages | scripts/backup:11-52 |
| Restore | scripts/restore | arquivo de backup válido e fonte disponível | reinstala latest, restaura banco/config, check sanitizado e Pages | scripts/restore:11-139 |
| Change URL | scripts/change_url | novo domínio/path | altera Nginx e gitlab.rb, reconfigura e reinicia | scripts/change_url:7-61 |
| Config | scripts/config | parâmetros Pages/use_web_account | atualiza permissões/configuração e reconfigura | scripts/config:19-114 |
| Remove | scripts/remove | autorização para operação destrutiva | remove serviço, pacote, config, dados e swap | scripts/remove:7-71 |
| Health | scripts/install, upgrade, restore | logs/serviço disponíveis | espera Puma; restore executa gitlab:rake gitlab:check | paths acima |

## Riscos priorizados

| ID | Nível | Condição observada | Consequência | Próxima prova |
|---|---|---|---|---|
| GL-R-01 | P0 | workflow não compatível com master-only e pode não executar por falta de yq/jinja2 | updates não produzem proposta revisável ou violam governança | workflow em runner limpo, sem publicar release |
| GL-R-02 | P1 | generator e consumidor do upgrade path são parsers distintos sem contrato diferencial | salto, parada ou asset incorreto pode quebrar upgrade | testes de grafo com fixtures oficiais |
| GL-R-03 | P1 | patch de gitlab.rb não verifica matches | template upstream pode mudar sem falha explícita | teste que remove cada linha-alvo e exige erro |
| GL-R-04 | P1 | restore reinstala latest, não o build do backup | incompatibilidade de schema/migração ou restauração incompleta | restore de backups produzidos por versões suportadas |
| GL-R-05 | P1 | instalação/upgrade alteram sysctl, swap, serviço, Nginx e dados | efeito amplo no host e risco de estado parcial | lifecycle em snapshot YunoHost com rollback |
| GL-R-06 | P1 | remove apaga /var/opt/gitlab e o swap do app | perda de dados se backup/gate falhar | teste destrutivo apenas em namespace efêmero |
| GL-R-07 | P2 | Pages usa domínio dedicado e permission dinâmica | colisão com outro app ou configuração órfã | matriz enable/disable/change-domain/restore |
| GL-R-08 | P2 | não há conf/gitlab.<major>.rb no snapshot embora upgrade procure por ele | caminho de mitigação de migração nunca foi demonstrado | fixture de major que exija configuração intermediária |
| GL-R-09 | P2 | CI só chama package_linter, sem gerador/lifecycle | regressões funcionais passam no CI | harness de package_check e testes de gerador |

## Superfícies sensíveis

- GitLab secrets e banco são tratados pelo backup/restore, mas não foram
  manipulados neste ambiente.
- LDAP é habilitado no template e usa filtro/permissão YunoHost em
  conf/gitlab.rb:589-661; a configuração real depende do diretório do host.
- gitlab.rb é regenerado durante upgrade, change-url e config; a separação
  entre configuração gerada e gitlab-persistent.rb é uma invariante operacional.
- Nginx e GitLab usam portas internas fixadas no manifest e proxies locais.
- remove e restore são operações com impacto externo e exigem ambiente
  controlado; não foram executadas nesta rodada.

## Cobertura atual versus necessária

| Área | Observado | Necessário para aceite futuro |
|---|---|---|
| Sintaxe | TOML, shell e Python compilam | package_linter e schema YunoHost |
| Fontes | URLs/hash estruturalmente completos; amostras HTTP 200 | download/hash de todos os assets ou prova equivalente |
| Instalação | script lido | install CE/EE amd64/arm64 em YunoHost |
| Upgrade | lógica lida; floor 16.9 explícito | caminhos de cada major e migrações longas |
| Backup/restore | paths e comandos lidos | backup real, restore real e verificação de dados |
| Pages/URL/config | branches de script lidas | matriz de transições e rollback |
| Segurança | nenhum segredo detectado no GitLab | redaction de logs e inspeção de arquivos gerados |
