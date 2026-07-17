# Handoff atual

Estado: `READY_FOR_CODEX_CONTINUOUS_ROUND`  
Charter: `CHR-GOV-AUTONOMY-001`  
Branch: `master`

## Prompt

```text
Leia AGENTS.md e continue.
```

## Entrada

1. Reconciliar `origin/master` do coordenador e Runner.
2. Confirmar o charter `READY` em `continuity/ACTIVE_ROUND.md`.
3. Ler os quatro acceptance packs publicados pelo Orquestrador.
4. Atribuir novo `Round-ID`.
5. Iniciar no mínimo duas lanes independentes e registrar ownership/tempos.
6. Integrar e publicar uma tarefa por vez.
7. Após o motor ficar GREEN, migrar e consumir a fila canônica enquanto houver trabalho elegível.

## Baselines de preparação

- coordinator acceptance head antes do charter: `f6dd35b0b30cb72505a6e4a6d7eb0e2b689566a8`;
- Runner acceptance head antes do charter: `17be5e890010c2eb96d857713f2bc0164092b943`.

## Prioridade

1. motor de execução contínua;
2. default Alpine suportado;
3. autoupdate GitLab;
4. foundation MCP;
5. trust/CI Runner e migração do backlog.

Não alterar os acceptance tests do Orquestrador. Não declarar `ACCEPTED`.
