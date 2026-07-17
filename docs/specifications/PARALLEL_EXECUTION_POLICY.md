# Política de paralelismo substantivo

## Separabilidade

Paths são normalizados e comparados por ancestralidade. `evidence/` conflita com `evidence/mcp/`; strings diferentes não bastam. Tarefas no mesmo repositório só são paralelas quando seus ownerships são disjuntos por prefixo. Tarefas em repositórios diferentes continuam sujeitas a outputs compartilhados declarados.

## Lanes

O planner gera lanes para tarefas elegíveis. Para cada lane, o Executor usa:

```text
python scripts/maestro_program.py lane-start ...
python scripts/maestro_program.py lane-finish ...
python scripts/maestro_program.py validate-wave ...
```

O journal é hash-chained. A validação exige workers distintos, overlap, artifact e command log hashados. Timestamps manuais em Markdown não são prova suficiente.

## Subagentes

Subagentes trabalham em cópias/snapshots isolados, sem commit, push, edição de arquivos canônicos ou expansão de escopo. Entregam patch/artifact, log, testes, unknowns e dead ends. O Executor integra uma tarefa por vez.

## Integração

Commits e pushes permanecem seriais. Antes de cada commit, o Executor reconcilia o remoto, valida ownership, oracles, gates e receipt.
