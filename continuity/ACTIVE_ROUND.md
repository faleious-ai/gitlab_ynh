# Rodada ativa

Charter-ID: `CHR-WP01-001`  
Estado: `READY`  
Preparado em: 2026-07-16  
Orquestrador: ChatGPT com o Maestro Diretor  
Executor principal: Codex  
Work Package: `WP-01 — Auditoria baseline`

## Autorização de entrada

O prompt `Leia AGENTS.md e continue` autoriza a execução integral deste charter. O `Round-ID` no formato `RND-YYYYMMDD-NNN` deve ser atribuído no START e repetido nos dois repositórios.

## Perguntas prévias

Nenhuma pergunta humana adicional é necessária. A rodada é investigativa, reversível, não modifica versões nem comportamento de instalação e possui critérios suficientes.

## Objetivo

Produzir baseline verificável e integrado de `gitlab_ynh` e `gitlab-runner_ynh`, divergência contra upstream, mapa de lifecycle, riscos, lacunas de autoupdate/testes e backlog técnico derivado. Não implementar updater nesta rodada.

## Escopo

### WP-01A — GitLab YunoHost

- inventariar manifest, sources, scripts, templates/config, serviços, permissões, testes, workflows e documentação;
- mapear CE/EE × Debian × arquitetura × versão/hash;
- mapear install, upgrade, backup, restore, change-url, config, remove e health;
- localizar dependências de versão e riscos de caminho obrigatório de upgrade.

### WP-01B — Runner YunoHost

Executar no repositório relacionado o inventário integral definido no charter local, incluindo runner/helper images, tokens, Docker/executor e lifecycle.

### WP-01C — Upstream

Comparar ambos os forks com os upstreams YunoHost e classificar diferenças como herdada, local deliberada, atualização pendente, incompatibilidade ou documentação.

### WP-01D — Síntese

- produzir mapa de riscos e lacunas de assurance;
- derivar backlog técnico ordenado com critérios de aceite;
- registrar desconhecidos sem inventar completude;
- reconciliar a síntese cross-repo.

## Fora de escopo

- alterar versão, URL, hash ou comportamento;
- implementar autoupdate;
- usar tokens reais ou registrar Runner em produção;
- criar mirrors/repositórios;
- alterar ruleset, visibilidade, licença ou fork network.

## Grafo paralelo

### Onda 1 — paralela

- Frente A: estrutura, manifest e source matrix de `gitlab_ynh`.
- Frente B: lifecycle, configuração, testes e workflows de `gitlab_ynh`.
- Frente C: inventário completo de `gitlab-runner_ynh`.
- Frente D: upstreams, histórico e divergências dos dois forks.

Cada frente deve possuir ownership de outputs sem editar o mesmo arquivo canônico. Subagentes não fazem commit.

### Gate de integração 1

O executor principal verifica paths/commits, remove duplicação, resolve contradições e identifica lacunas.

### Onda 2 — paralela

- síntese de riscos GitLab;
- síntese de riscos Runner;
- lacunas de testes/assurance;
- backlog derivado e dependências.

### Gate final

Validação cruzada, consistência dos documentos, atualização de continuidade e commits coordenados.

## Outputs obrigatórios

Em `gitlab_ynh`:

- `docs/audit/GITLAB_PACKAGE_BASELINE.md`;
- `docs/audit/UPSTREAM_DIVERGENCE.md`;
- `docs/audit/AUTOUPDATE_GAPS.md`;
- `docs/audit/LIFECYCLE_AND_RISK_MAP.md`;
- `docs/audit/CROSS_REPO_BASELINE.md`.

Em `gitlab-runner_ynh`:

- `docs/audit/RUNNER_PACKAGE_BASELINE.md`;
- `docs/audit/UPSTREAM_DIVERGENCE.md`;
- `docs/audit/AUTOUPDATE_GAPS.md`;
- `docs/audit/LIFECYCLE_AND_SECURITY_MAP.md`.

Nos dois: status, handoff, evidence index e round record.

## Definition of Done

- todos os itens de escopo possuem fato, path/fonte e estado de verificação;
- matrizes não possuem combinações silenciosamente omitidas;
- desconhecidos e limitações estão explícitos;
- nenhuma implementação funcional foi misturada;
- backlog possui dependência e critério observável;
- validação documental e reconciliação cross-repo foram executadas;
- um commit em `master` por repositório, mesmo `Round-ID`;
- estado final do Codex: `EXECUTED_AWAITING_REVIEW`.

## Bloqueio válido

Somente missão/visibilidade/licença, segredo indispensável, operação irreversível, escolha de produto com consequência material ou fonte indispensável inacessível após tentativas documentadas. Antes de parar, concluir todas as outras frentes do DAG.

## Pacote de revisão

Entregar commits, matriz tarefa → output → evidência, comandos/métodos, gaps, riscos residuais, bloqueios e recomendação de próxima rodada. Não declarar `ACCEPTED`.
