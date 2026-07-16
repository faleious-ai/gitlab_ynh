# Handoff atual

Estado: `READY_FOR_WP_01`  
Round anterior: `RND-20260716-001`  
Branch: `master`

## Retomada mínima

1. Leia `AGENTS.md`.
2. Confirme que o HEAD atual de `master` contém este arquivo.
3. Leia `continuity/STATUS.md`.
4. Leia apenas as seções `WP-01A` e `WP-01B` de `continuity/EXECUTION_PLAN.md`.
5. Para critérios, leia `docs/specifications/WORK_BREAKDOWN.md` e `docs/specifications/GITLAB_PACKAGE_AUTOUPDATE_SPEC.md` somente onde a auditoria exigir.

## Trabalho concluído

A infraestrutura MAESTRO foi instalada sem alterar scripts, manifesto ou comportamento do pacote. A memória agora está dividida entre contexto estável, status atual, decisões, plano, evidências e registros append-only de rodada.

## Próxima unidade executável

### WP-01A — Inventário local de `gitlab_ynh`

Produzir:

- `docs/audit/GITLAB_PACKAGE_BASELINE.md`;
- inventário de `manifest.toml`, scripts, configurações, testes, workflows e documentação;
- matriz CE/EE × Debian × arquitetura × versão;
- fluxo de install/upgrade/backup/restore/change-url/remove;
- pontos que dependem de versão e possíveis riscos de autoupdate.

### WP-01B — Inventário coordenado de `gitlab-runner_ynh`

Executar no repositório relacionado e produzir o conjunto local equivalente. Neste repositório, registrar apenas síntese e referência cruzada em `docs/audit/CROSS_REPO_BASELINE.md`.

### WP-01C — Divergência de upstream

Comparar cada fork com seu upstream YunoHost e classificar diferenças como:

- herdada;
- local deliberada;
- atualização pendente;
- incompatibilidade;
- documentação apenas.

## Condições de parada

Pare e peça decisão humana somente se ocorrer uma destas situações:

- necessidade de mudar missão, licença, visibilidade ou fork network;
- acesso a segredo ou credencial não provisionada;
- operação destrutiva ou irreversível;
- divergência entre upstream e fork que exija escolher uma política de produto com consequência prática relevante;
- impossibilidade de obter fonte necessária após registrar tentativas e alternativas.

## Fechamento da próxima rodada

O commit deve conter, no mesmo conjunto atômico:

- documentos de auditoria;
- atualização de `STATUS.md`;
- novo `HANDOFF_CURRENT.md`;
- atualização de `EVIDENCE_INDEX.md`;
- novo registro em `continuity/rounds/`;
- trailer `Round-ID: RND-YYYYMMDD-NNN`.

Não crie branch nem PR.