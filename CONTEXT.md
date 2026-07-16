# Contexto canônico

## Propósito

Este repositório mantém o empacotamento YunoHost do GitLab e atua, temporariamente, como coordenador do programa que inclui:

1. autoupdate seguro e reproduzível de `gitlab_ynh`;
2. autoupdate coordenado de `gitlab-runner_ynh`;
3. espelhos somente leitura dos upstreams GitLab no GitHub;
4. um MCP GitLab com cobertura ampla e mensurável das APIs REST e GraphQL;
5. assurance, segurança, evidência e continuidade entre agentes.

## Estado de origem

- Repositório local de coordenação: `faleious-ai/gitlab_ynh`.
- Repositório relacionado: `faleious-ai/gitlab-runner_ynh`.
- Upstream do pacote: `YunoHost-Apps/gitlab_ynh`.
- Upstreams de produto: `gitlab-org/gitlab` e `gitlab-org/gitlab-runner` no GitLab.
- Issue coordenadora: `faleious-ai/gitlab_ynh#1`.
- Plano histórico inicial: `docs/planning/GITLAB_MCP_AND_AUTOUPDATE_PLAN.md`.

## Tese operacional

“Apontar para a versão mais recente” significa descobrir automaticamente a versão estável elegível, validar caminho de upgrade, resolver todos os assets, fixar URLs e hashes e produzir uma mudança revisável. Nunca significa baixar `latest` em tempo de instalação.

## Autoridades

- `manifest.toml`, scripts, testes e configurações: comportamento real do pacote.
- `docs/specifications/`: contratos de trabalho e critérios de aceite.
- `docs/decisions/` e `continuity/DECISIONS.md`: rationale vigente.
- `continuity/STATUS.md`: fotografia factual atual.
- `continuity/HANDOFF_CURRENT.md`: ponto de retomada.
- `evidence/EVIDENCE_INDEX.md`: provas verificáveis.
- Git e registros de rodada: proveniência.

## Restrições permanentes

- branch única `master`;
- um commit por rodada de IA e por repositório afetado;
- sem force push;
- sem segredos;
- sem atualização não fixada;
- sem saltar etapas obrigatórias de upgrade;
- sem declarar cobertura MCP sem operação, permissão e teste correspondentes;
- operações destrutivas apenas em namespace efêmero e com gate explícito.

## Definição de continuidade

Qualquer agente deve conseguir retomar o trabalho lendo `AGENTS.md`, `HANDOFF_CURRENT.md` e `STATUS.md`, expandindo o contexto somente pelas rotas indicadas. O chat pode ajudar na execução, mas não substitui a memória persistida.