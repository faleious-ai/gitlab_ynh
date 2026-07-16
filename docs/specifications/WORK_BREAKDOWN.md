# Divisão do trabalho

## Convenções

- `Owner`: repositório que possui a implementação.
- `Depends`: unidades que precisam estar concluídas.
- `Gate`: `A` autonomia técnica, `B` autonomia com ADR/evidência reforçada, `C` decisão humana antes da ação.
- Toda unidade fecha com um commit de rodada em `master`.

## Backlog executável

| ID | Unidade | Owner | Depends | Gate | Saída principal |
|---|---|---|---|---|---|
| WP-00 | Bootstrap MAESTRO | gitlab_ynh + runner | — | A | memória, decisões, protocolo e specs |
| WP-01A | Inventário GitLab YNH | gitlab_ynh | WP-00 | A | baseline local completo |
| WP-01B | Inventário Runner YNH | runner | WP-00 | A | baseline local completo |
| WP-01C | Divergência upstream | ambos | 01A/01B | A | matriz de drift |
| WP-01D | Lacunas e riscos | ambos | 01C | B | backlog derivado e prioridade |
| WP-02A | Fonte de release Runner | runner | WP-01 | B | ADR e fixtures |
| WP-02B | Resolver runner + helpers | runner | 02A | A | resolução atômica |
| WP-02C | Gerador de manifest Runner | runner | 02B | A | diff determinístico |
| WP-02D | Testes e lifecycle Runner | runner | 02C | A/B | evidência executável |
| WP-03A | Fonte de release GitLab | gitlab_ynh | WP-01 | B | ADR e fixtures |
| WP-03B | Grafo de upgrade path | gitlab_ynh | 03A | B | resolver e casos |
| WP-03C | Resolver matriz CE/EE | gitlab_ynh | 03A | A | assets/hashes |
| WP-03D | Gerador de manifest GitLab | gitlab_ynh | 03B/03C | A | diff determinístico |
| WP-03E | Testes e lifecycle GitLab | gitlab_ynh | 03D | A/B | evidência executável |
| WP-04A | Criar mirrors | ambiente autorizado | WP-00 | C | repos de mirror |
| WP-04B | Sync auditável | mirror/runner | 04A | B | job, logs e estado |
| WP-05A | Criar `gitlab-mcp` | GitHub autorizado | WP-00 | C | repo coordenador MCP |
| WP-05B | Migrar autoridade MCP | gitlab-mcp | 05A | B | contexto, ADRs e handoff |
| WP-06A | Extrair REST | gitlab-mcp | 05B | A | catálogo REST |
| WP-06B | Extrair GraphQL | gitlab-mcp | 05B | A | catálogo GraphQL |
| WP-06C | Matriz version/edition/scope | gitlab-mcp | 06A/06B | B | availability matrix |
| WP-06D | Paridade GitHub | gitlab-mcp | 06C | A | gap report |
| WP-07A | Núcleo transporte/auth | gitlab-mcp | WP-06 | B | cliente version-aware |
| WP-07B | Descoberta e leitura | gitlab-mcp | 07A | A | wave 1 |
| WP-07C | Colaboração/work items | gitlab-mcp | 07B | A | wave 2 |
| WP-07D | Repo/commits/refs | gitlab-mcp | 07B | B | wave 3 |
| WP-07E | CI/CD/artifacts | gitlab-mcp | 07B | B | wave 4 |
| WP-07F | Releases/packages | gitlab-mcp | 07B | B | wave 5 |
| WP-07G | Administração permitida | gitlab-mcp | 07B | C para operações R3 | wave 6 |
| WP-08A | Contract harness | gitlab-mcp | 07A | B | suíte isolada |
| WP-08B | Segurança/redaction | gitlab-mcp | 08A | B | testes negativos |
| WP-08C | Coverage gate | gitlab-mcp | WP-06/07/08 | B | relatório automático |
| WP-09 | Release e manutenção | todos | WP-02/03/08 | C para produção/release | operação contínua |

## Critérios de aceite por grupo

### Auditoria

- inventário de arquivos e lifecycle;
- fatos citados por path/linha/commit quando possível;
- divergências classificadas;
- desconhecidos explícitos;
- nenhuma implementação misturada.

### Updaters

- determinismo;
- idempotência;
- matriz completa;
- hashes;
- falha fechada;
- testes de casos positivos e negativos;
- lifecycle proporcional.

### MCP

- catálogo antes de declarar cobertura;
- version/edition awareness;
- auth/policy por operação;
- tools e residual API sem URL arbitrária;
- contract tests;
- auditabilidade;
- coverage report.

## Prioridade

1. WP-01;
2. WP-02;
3. WP-03;
4. WP-04/05 quando ambiente permitir;
5. WP-06;
6. WP-07 e WP-08 em paralelo controlado;
7. WP-09.

## Regra anti-fragmentação

O agente não deve abrir microtarefas para cada arquivo. Deve executar a maior unidade coerente cuja validação e commit permaneçam compreensíveis. Dividir somente por dependência, risco, ambiente ou gate humano real.