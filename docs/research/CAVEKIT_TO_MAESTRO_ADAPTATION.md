# Relatório de adaptação Cavekit → MAESTRO

Data: 2026-07-16  
Round: `RND-20260716-009`  
Fonte principal: `JuliusBrussee/cavekit`

## Material lido

Cavekit v4 no commit `c322f0bb6db82163041930467f3ce32754d42827`:

- `FORMAT.md`;
- `skills/spec`;
- `skills/build`;
- `skills/check`;
- `skills/grill`;
- `skills/research`;
- `skills/review`;
- `skills/deepen`;
- `skills/caveman`;
- `skills/backprop`.

Cavekit v3.1.0:

- `methodology`;
- `validation-first`;
- `peer-review`;
- `context-architecture`;
- `revision`;
- `convergence-monitoring`;
- `impl-tracking`;
- `speculative-pipeline`;
- `autonomous-loop`;
- `karpathy-guardrails`.

## Princípios adotados

| Origem | Adaptação MAESTRO |
|---|---|
| spec durável | charters/especificações continuam distribuídos por autoridade; ownership de escrita fica explícito |
| verification contract | cada claim nomeia seam, teste/comando, resultado e nível de evidência |
| TDD-within-SDD | RED→GREEN obrigatório para mudança comportamental, inclusive shell/config/packaging |
| backprop | falha classificada retroalimenta critério, invariante, teste e memória |
| adversarial review | challenge pré-build em alto impacto + dois eixos pré-commit + revisão externa ChatGPT |
| drift check | verificador read-only distingue forma, comportamento, CI e lifecycle |
| research | fonte primária por claim; unknown permanece explícito |
| deepen | refatoração estrutural em tarefa própria, suíte verde antes/depois |
| caveman | compressão apenas em matrizes/ledgers sem risco de ambiguidade |
| convergence | medir claims, gates, findings e bloqueios; diff apenas sinal secundário |
| implementation tracking | dead ends e causas preservados; sem duplicar status/handoff |
| task commits | tarefa é unidade de commit, sincronização e reversão; rodada é unidade de autorização/revisão |

## Princípios rejeitados ou substituídos

| Escolha Cavekit | Decisão local |
|---|---|
| um único `SPEC.md` | memória MAESTRO em camadas e progressive disclosure |
| v4 sem subagentes/paralelismo | manter DAG e subagentes com ownership, inspirados no v3 |
| commit por subagente/tarefa em branch | executor integra e publica commit de tarefa diretamente em `master`; subagentes não commitam |
| aprovação humana para todo backprop | autonomia técnica; humano apenas para consequência material |
| hooks/runtime Claude-specific | não instalar; importar invariantes de estado, lock, budget e retomada |
| linhas de diff como principal convergência | coverage de claims/gates/findings precede tamanho do diff |
| grep como verificação suficiente | busca textual é apenas `STRUCTURALLY_OBSERVED` |
| compressão ampla | proibir em segurança, ADR, gate humano e recuperação |

## Skills locais resultantes

1. `maestro-spec`;
2. `maestro-build`;
3. `maestro-check`;
4. `maestro-grill`;
5. `maestro-research`;
6. `maestro-review`;
7. `maestro-deepen`;
8. `maestro-caveman`;
9. `maestro-backprop`;
10. `maestro-tdd`;
11. `maestro-convergence`;
12. `maestro-guardrails`.

As skills executáveis residem no repositório funcional `gitlab-runner_ynh` durante WP-02. O coordenador mantém este relatório, ADR-0006 e os protocolos transversais.

## Decisões do Maestro Diretor

- commits por tarefa aprovados;
- TDD obrigatório em toda mudança comportamental;
- backprop técnico automático;
- revisão pré-commit em dois eixos;
- Caveman limitado;
- convergência como gate operacional;
- autonomia MAESTRO preservada.

## Licença e atribuição

Cavekit é MIT, Copyright (c) 2026 Julius Brussee. As skills locais são adaptações substantivas para este programa e preservam a atribuição no repositório funcional.
