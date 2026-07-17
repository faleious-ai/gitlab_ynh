# Especificação executável da arquitetura de trabalho v2

Status: `ORCHESTRATOR_OWNED`

## Objetivo

A invocação do Executor deve consumir o backlog completo do programa, e não apenas uma lista manual da rodada. A execução continua por todas as tarefas técnicas reversíveis elegíveis, cria correções para findings acionáveis e só encerra como conclusão, gate humano válido ou checkpoint externo explícito.

## Fontes canônicas

1. `continuity/PROGRAM_MANDATE.json` — autoridade, proibições, ownership dos oracles e política de parada.
2. `continuity/PROGRAM_BACKLOG.json` — escopo integral, work packages, dependências, ownership e contratos de tarefa.
3. `continuity/PROGRAM_STATE.json` — decisões do Orquestrador, gates, bloqueios e histórico; não declara conclusão técnica por edição manual.
4. `continuity/PROGRAM_FINDINGS.json` — findings abertos, resolvidos e respectivas tarefas corretivas.
5. `continuity/PROGRAM_QUEUE.json` — snapshot derivado; nunca é autoridade de escopo.
6. receipts em `continuity/task_receipts/` — prova self-bound de tarefa publicada.

## Invariantes de parada

`eligible_tasks=[]` não basta. `stop_allowed=true` só pode ocorrer quando:

- todos os itens do backlog estão `accepted`/`superseded`; ou
- os únicos itens restantes possuem gate humano válido, completo e sob autoridade externa.

Review pendente ou ambiente indisponível permite apenas `checkpoint_allowed=true`, sem declarar conclusão. Finding acionável aberto, fila derivada stale, backlog incompleto, gate inválido, teste conhecido sem tarefa corretiva ou trabalho planejado não ativado mantêm `stop_allowed=false`.

## Estado técnico derivado

A conclusão de uma tarefa é derivada de um receipt `SELF`, incluído no mesmo commit da tarefa, cujo commit:

- contém o `Task-ID` no subject;
- está publicado em `origin/master` de todos os repositórios afetados;
- altera somente paths autorizados e o receipt;
- contém evidências e gates `pass` no próprio commit.

O Executor não pode editar `PROGRAM_STATE.json` para fabricar `completed`.

## Proteção de oracles

A proteção é calculada pelo diff Git real, com detecção de arquivos modificados, criados, removidos e renomeados. O mandato mantém prefixos protegidos e inventário SHA-256. O Executor não fornece a lista de paths que deseja validar.

## Paralelismo substantivo

Quando tarefas são separáveis por repositório e ownership prefix-aware, o plano exige pelo menos duas lanes. Cada lane precisa de:

- worker distinto;
- start/finish em journal hash-chained;
- intervalos realmente sobrepostos;
- artifact não vazio com SHA-256;
- command log não vazio com SHA-256;
- paths idênticos ao ownership do plano.

Rodar apenas testes RED simultaneamente não prova desenvolvimento paralelo. Subagentes preparam outputs em cópias isoladas; o Executor integra, valida, commita e publica serialmente.

## Findings e backprop

Finding técnico reversível acionável deve possuir `correction_task_id`. `register-finding` cria finding e tarefa corretiva canônica. Finding aberto sem correção torna o programa inválido.

## Acceptance

`tests/acceptance/test_autonomous_program_execution.py` verifica:

- backlog fora da queue impede falso stop;
- finding aberto impede stop;
- diff Git real protege oracles, inclusive rename e prefixo;
- conflitos ancestral/descendente impedem paralelismo falso;
- lanes exigem workers, overlap, artifacts e logs hashados;
- tarefa só conclui após receipt self-bound publicado;
- checkpoint não é conclusão;
- finding cria tarefa corretiva;
- drift de hash e cobertura incompleta invalidam o programa.
