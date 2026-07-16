# Limites entre repositórios

## Mapa

### `faleious-ai/gitlab_ynh`

Autoridade sobre:

- empacotamento YunoHost do GitLab;
- política de versões e upgrade path do pacote GitLab;
- coordenação temporária do programa;
- issue principal e decisões transversais até existir `gitlab-mcp`.

Não deve conter:

- implementação principal do servidor MCP;
- cópia completa dos upstreams GitLab;
- credenciais de instância ou runner;
- código do pacote Runner salvo integração estritamente necessária.

### `faleious-ai/gitlab-runner_ynh`

Autoridade sobre:

- empacotamento YunoHost do GitLab Runner;
- resolução atômica de runner e helper images;
- registro, executor, serviço, upgrade e lifecycle do Runner;
- testes e evidências locais do pacote.

### futuro `faleious-ai/gitlab-mcp`

Autoridade sobre:

- servidor MCP;
- clientes REST/GraphQL;
- catálogo machine-readable de API;
- tools e workflows;
- autorização, policy engine, auditoria e redaction;
- contract tests e matriz de cobertura/paridade.

Quando criado, decisões específicas do MCP migram para ele. Este repositório mantém somente referências e contratos de integração.

### mirrors upstream

Autoridade: nenhuma decisão local de produto.

São cópias somente leitura de `gitlab-org/gitlab` e `gitlab-org/gitlab-runner`, atualizadas por sincronização auditável. Alterações manuais são proibidas.

## Transações cross-repo

Uma mudança que afete mais de um repositório deve:

1. usar o mesmo `Round-ID`;
2. declarar a ordem dos commits;
3. registrar versões/contratos compatíveis;
4. deixar cada repositório isoladamente compreensível;
5. atualizar o handoff em todos os repositórios afetados;
6. registrar estado parcial se um commit subsequente falhar;
7. nunca usar force push para alinhar históricos.

## Autoridade de versão

- versão do GitLab: manifest e updater em `gitlab_ynh`;
- versão do Runner e helper images: manifest/updater em `gitlab-runner_ynh`;
- versões suportadas da API MCP: catálogo e compatibility matrix em `gitlab-mcp`;
- compatibilidade cruzada: documento explícito, nunca inferência pelo número mais recente.

## Drift

Drift é qualquer divergência não registrada entre:

- fork e upstream YunoHost;
- pacote e versão publicada do produto;
- Runner e helper images;
- catálogo MCP e API da instância alvo;
- especificação e comportamento testado;
- status/handoff e HEAD real.

Toda auditoria deve classificar drift, impacto, urgência e plano de correção.