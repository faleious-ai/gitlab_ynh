# Rodada ativa

Charter-ID: `CHR-GOV-AUTONOMY-001`  
Estado: `READY`  
Preparado em: 2026-07-17  
Executor principal: Codex  
Unidade: `fila técnica contínua orientada por acceptance tests`

## Baseline

- coordenador: `f6dd35b0b30cb72505a6e4a6d7eb0e2b689566a8`;
- Runner: `17be5e890010c2eb96d857713f2bc0164092b943`.

Resolver novamente `origin/master` no START e admitir commits posteriores legítimos.

## Autorização

`Leia AGENTS.md e continue` autoriza todas as tarefas técnicas, reversíveis e sem efeito externo desta rodada. Cada tarefa concluída gera commit remoto próprio. O Executor continua pelas dependências elegíveis e só encerra depois de concluir ou classificar todo trabalho independente deste charter.

## Especificações executáveis protegidas

O Executor executa, mas não reduz nem remove:

- `docs/specifications/AUTONOMOUS_PROGRAM_EXECUTION_SPEC.md`;
- `tests/acceptance/test_autonomous_program_execution.py`;
- `docs/specifications/GITLAB_AUTOUPDATE_ACCEPTANCE.md`;
- `tests/acceptance/test_gitlab_autoupdate_objective.py`;
- `docs/specifications/GITLAB_MCP_FOUNDATION_ACCEPTANCE.md`;
- `tests/acceptance/test_gitlab_mcp_foundation.py`;
- Runner `tests/acceptance/test_supported_docker_default.py`.

Divergência real produz `TEST_CONTRACT_CHALLENGE`; as demais tarefas continuam.

## Onda paralela inicial

Executar em ambientes isolados e integrar serialmente:

1. `T-GOV-01-program-engine`: implementar `scripts/maestro_program.py` e os arquivos canônicos de mandato, fila e estado até o acceptance do motor ficar GREEN.
2. `T-RUN-01-supported-docker-default`: tornar GREEN o acceptance Alpine usando tag patch observada e ainda suportada.
3. `T-GITLAB-01-autoupdate-engine`: implementar `scripts/gitlab_autoupdate.py` até o acceptance do updater ficar GREEN, sem promover manifest.
4. `T-MCP-01-foundation`: preparar o servidor GitLab MCP separado em test mode até o acceptance de fundação ficar GREEN ou produzir pacote publicável quando o repositório remoto não puder ser criado pelo ambiente.
5. `T-RUN-02-observability`: continuar diagnóstico read-only de confiança live e CI, preservando estados não observados.

Quando houver duas ou mais frentes independentes, iniciar no mínimo duas lanes e registrar `Lane-ID`, ownership, baseline, início, término, RED/GREEN e output. A integração, o commit e o push permanecem seriais.

## Integração do processo

Após T-GOV-01:

- atualizar `AGENTS.md`, protocolos, arquitetura e políticas dos dois repositórios;
- fazer a invocação carregar a fila canônica, em vez de depender apenas de um charter isolado;
- migrar os work packages restantes para o DAG;
- fazer findings criarem tarefas corretivas prioritárias;
- permitir que tarefas reversíveis independentes continuem enquanto uma revisão está pendente;
- rejeitar parada por limitação meramente técnica quando existir trabalho independente.

## Fila inicial mínima

A fila canônica deve incluir:

- correção Alpine;
- nova observação da confiança Runner;
- observação de CI por SHA;
- autoupdate GitLab CE/EE e required stops;
- catálogo live GitLab sem promoção;
- foundation GitLab MCP;
- inventário REST/GraphQL;
- harnesses das próximas ondas;
- assurance e manutenção.

Itens sem acceptance protegido podem avançar por pesquisa, fixture, modelagem e harness, mas não declarar o objetivo funcional concluído.

## Limites

- somente trabalho técnico reversível e não operacional;
- sem release, deploy ou promoção;
- sem alteração de ambiente real;
- sem branch, PR, worktree, squash, force push ou reescrita;
- o Executor não declara `ACCEPTED`.

## Fechamento

Entregar os acceptance results, matriz task→commit→claim→evidência, prova de lanes paralelas ou justificativa objetiva, fila migrada, HEADs reconciliados e estado remoto retomável. O estado final é `EXECUTED_AWAITING_REVIEW` ou checkpoint explícito de fila ainda em execução.
