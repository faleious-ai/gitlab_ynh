# Handoff atual

Estado: `EXECUTED_AWAITING_REVIEW`
Charter executado: `CHR-WP01-001`
Round concluído: `RND-20260716-003`
Branch: `master`

## Prompt de retomada

Use exatamente:

```text
Leia AGENTS.md e continue.
```

Uma orientação adicional pode ser anexada, mas o Codex deve reconciliá-la com o charter ativo e registrá-la no round record.

## Retomada mínima do Codex

1. Ler `AGENTS.md`.
2. Confirmar HEAD de `master` nos dois repositórios.
3. Ler `continuity/STATUS.md` e `continuity/ACTIVE_ROUND.md`.
4. Confirmar o estado persistido e consultar o revisor antes de abrir nova rodada.

## Rodada executada

`WP-01A/B/C/D — Auditoria baseline completa dos dois instaladores`.

O charter definiu e a execução concluiu quatro frentes paralelas iniciais:

- estrutura/manifest/sources do GitLab;
- lifecycle/testes/workflows do GitLab;
- inventário completo do Runner;
- upstream e divergências dos dois forks.

Após integração, foram executadas as sínteses de riscos, assurance e backlog.
O updater não foi implementado.

## Regra de esforço

O Codex não deve parar para fornecer progresso. Deve concluir todas as tarefas não bloqueadas, tentar alternativas técnicas e continuar frentes independentes. Só pode parar após:

- conclusão integral e commits coordenados; ou
- conclusão de todo trabalho independente e registro de bloqueio humano válido.

## Subagentes

Use subagentes para frentes independentes. Eles não fazem commit, não alteram arquivos canônicos compartilhados sem ownership e não expandem escopo. O Codex integra, verifica e valida.

## Estado de saída

`EXECUTED_AWAITING_REVIEW`.

O Codex entregou commits, evidências, matriz tarefa-output-evidência, gaps,
riscos residuais e bloqueios. Não marcou `ACCEPTED`.

## Revisão

O ChatGPT deve revisar o trabalho via repositório. Se houver lacuna técnica,
definirá rodada corretiva completa. Se houver gate humano, apresentará ao
usuário alternativas, consequências e recomendação, persistirá a resolução e
liberará a continuação.

## Resultados para revisão

- Baseline GitLab: docs/audit/GITLAB_PACKAGE_BASELINE.md
- Divergência: docs/audit/UPSTREAM_DIVERGENCE.md
- Autoupdate: docs/audit/AUTOUPDATE_GAPS.md
- Lifecycle/risco: docs/audit/LIFECYCLE_AND_RISK_MAP.md
- Síntese cross-repo: docs/audit/CROSS_REPO_BASELINE.md

Achados principais: baseline GitLab 19.1.0~ynh1, candidato 19.1.2
disponível nos índices consultados, workflow herdado incompatível com
master-only, ausência de testes do gerador e lifecycle ainda não demonstrado.
