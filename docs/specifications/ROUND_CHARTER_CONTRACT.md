# Contrato de rodada completa

`continuity/ACTIVE_ROUND.md` é a autorização executável. A rodada define baseline, escopo, DAG, gates e intervalo de revisão. Cada tarefa é a unidade atômica de implementação, commit, sincronização e reversão.

## Estados

- `DRAFT`, `READY`, `IN_PROGRESS`;
- `TASK_LOCAL_COMPLETE_AWAITING_SYNC`;
- `TASK_REMOTE_SYNC_BLOCKED`;
- `BLOCKED_HUMAN`;
- `EXECUTED_AWAITING_REVIEW`;
- `ACCEPTED`, `CORRECTION_REQUIRED`, `SUPERSEDED`.

## Conteúdo obrigatório da rodada

- Charter-ID, objetivo, estado e baseline remoto;
- decisões humanas e técnicas vigentes;
- escopo, fora de escopo e repositórios autorizados;
- DAG de tarefas e ondas paralelas;
- gates, riscos, rollback e Definition of Done integrada;
- plano de persistência remota e pacote de revisão.

## Conteúdo obrigatório de cada tarefa

- `Task-ID` único e citado no commit;
- resultado verificável e reversível;
- dependências;
- seam público;
- claims/invariantes e interfaces tocadas;
- paths autorizados e ownership;
- contrato RED→GREEN quando houver mudança comportamental;
- comandos/gates e nível de evidência esperado;
- revisão Spec/Charter e Engineering;
- condição de commit e rollback;
- commits correspondentes nos repositórios afetados.

Tarefa que não cabe em um commit coerente deve ser dividida antes do primeiro edit.

## TDD

Toda mudança comportamental deve ser observável por seam público. O executor registra teste/comando red-capable, RED antes do fix, implementação mínima, GREEN e regressão proporcional. Busca textual, teste tautológico ou acoplamento a detalhe interno não satisfaz o contrato.

## Backprop

Falha inesperada gera classificação, causa, critério/invariante quando necessário, teste de regressão e memória. Lacuna técnica reversível é corrigida autonomamente; alteração material de comportamento ou consequência volta ao Maestro Diretor.

## Revisão pré-commit

Toda tarefa recebe passagens independentes de conformidade Spec/Charter e Engineering/Security/Lifecycle. P0/P1 bloqueiam; demais findings são corrigidos ou justificados.

## Persistência

- um commit por tarefa concluída e por repositório afetado;
- push e verificação remota antes da próxima escrita no mesmo repositório;
- sem squash, branch, PR, worktree, force push ou reescrita publicada;
- última tarefa da rodada reconcilia continuidade e evidências;
- revisão recebe a lista completa entre `baseline_head` e `round_head`.

## Preparação

O ChatGPT pergunta ao usuário apenas o que altera comportamento, compatibilidade, ambiente, custo, segurança, privilégio, publicação ou irreversibilidade. Questões técnicas reversíveis são decididas e justificadas pelo orquestrador.

## Saída

O Codex encerra conforme o estado real. Somente o orquestrador registra `ACCEPTED` após revisar cada commit e o resultado integrado.
