# Handoff atual

Estado: `READY_FOR_CODEX_FULL_ROUND`  
Charter ativo: `CHR-WP01-001`  
Round de governança anterior: `RND-20260716-002`  
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
4. Confirmar `Charter-ID: CHR-WP01-001` e estado `READY`.
5. Atribuir um `Round-ID` e executar integralmente o DAG.

## Rodada autorizada

`WP-01A/B/C/D — Auditoria baseline completa dos dois instaladores`.

O charter define quatro frentes paralelas iniciais:

- estrutura/manifest/sources do GitLab;
- lifecycle/testes/workflows do GitLab;
- inventário completo do Runner;
- upstream e divergências dos dois forks.

Após integração, executar sínteses paralelas de riscos, assurance e backlog. Não implementar updater.

## Regra de esforço

O Codex não deve parar para fornecer progresso. Deve concluir todas as tarefas não bloqueadas, tentar alternativas técnicas e continuar frentes independentes. Só pode parar após:

- conclusão integral e commits coordenados; ou
- conclusão de todo trabalho independente e registro de bloqueio humano válido.

## Subagentes

Use subagentes para frentes independentes. Eles não fazem commit, não alteram arquivos canônicos compartilhados sem ownership e não expandem escopo. O Codex integra, verifica e valida.

## Estado de saída esperado

`EXECUTED_AWAITING_REVIEW`.

O Codex entrega commits, evidências, matriz tarefa-output-evidência, gaps, riscos residuais e bloqueios. Não marca `ACCEPTED`.

## Revisão

O ChatGPT revisará o trabalho via repositório. Se houver lacuna técnica, definirá rodada corretiva completa. Se houver gate humano, apresentará ao usuário alternativas, consequências e recomendação, persistirá a resolução e liberará a continuação.
