# Handoff atual

Estado: `READY_FOR_CODEX_CORRECTION_ROUND`  
Charter ativo: `CHR-WP02-002`  
Revisão anterior: `REV-RND-20260716-005 — CORRECTION_REQUIRED`  
Branch: `master`

## Prompt

```text
Leia AGENTS.md e continue.
```

## Retomada mínima

1. Ler `AGENTS.md`.
2. Confirmar `master`, árvores limpas e `HEAD == origin/master` nos dois repositórios.
3. Ler `STATUS`, `ACTIVE_ROUND` e `continuity/reviews/REV-RND-20260716-005.md`.
4. Confirmar `CHR-WP02-002` em estado `READY`.
5. Executar o charter detalhado no repositório `faleious-ai/gitlab-runner_ynh`.

## Trabalho

Completar a cadeia de confiança do updater Runner: descoberta oficial, checksums, origem, manifest candidato/diff, credencial fora de argv, contrato YunoHost e CI verificável. Este coordenador recebe apenas síntese, decisão, evidências e continuidade.

## Regra de esforço

Não parar para progresso, pesquisa, teste falho ou primeira estratégia malsucedida. O gate histórico externo não bloqueia o trabalho técnico. Use subagentes nas frentes independentes definidas no charter Runner.

## Fechamento remoto

- um commit publicado em `origin/master` por repositório afetado, mesmo novo `Round-ID`;
- `HEAD == origin/master` e árvores limpas;
- arquivos/evidências acessíveis pelo GitHub;
- pacote de revisão com SHAs completos e URLs remotas;
- estado `EXECUTED_AWAITING_REVIEW`.

Não promover versão, registrar Runner real, criar branch/PR, executar ação destrutiva ou usar a credencial histórica.
