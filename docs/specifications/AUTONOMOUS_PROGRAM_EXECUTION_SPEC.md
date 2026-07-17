# Especificação de execução autônoma contínua

## Objetivo

Transformar a missão do programa em uma fila executável por máquina, permitindo ao Executor continuar por tarefas e work packages enquanto existir trabalho técnico reversível e autorizado. A execução só pode parar por conclusão real, interrupção ambiental total com estado seguro ou dependência exclusivamente humana demonstrada.

Esta especificação é normativa e complementa o mandato humano, os ADRs, o protocolo de rodada e as especificações funcionais. Ela não autoriza release, deploy, credenciais reais, custo, operação destrutiva ou mudança irreversível sem o gate correspondente.

## Ownership da especificação executável

O Orquestrador possui:

- este documento;
- `tests/acceptance/test_autonomous_program_execution.py`;
- os invariantes e resultados esperados desses testes.

O Executor pode executar o oracle, criar testes focais, implementar o motor, adicionar cenários mais estritos e abrir `TEST_CONTRACT_CHALLENGE`. Não pode enfraquecer assertions, remover cenários, alterar o seam ou reduzir gates para obter GREEN.

Mudança nesses paths pelo ator `executor` deve ser rejeitada pelo próprio motor, salvo um challenge versionado e aceito pelo Orquestrador.

## Seam público

O contrato é exercitado por:

```text
python3 scripts/maestro_program.py plan --mandate <json> --queue <json> --state <json>
python3 scripts/maestro_program.py validate-gate --mandate <json> --queue <json> --state <json> --gate <json>
python3 scripts/maestro_program.py validate-wave --plan <json> --evidence <json>
python3 scripts/maestro_program.py validate-change --mandate <json> --actor <ator> --paths <path>...
```

Toda saída normal é JSON em stdout. Erros de contrato usam código diferente de zero e JSON que explique o motivo sem segredo.

## Entradas canônicas futuras

O Executor implementará e manterá:

- `continuity/PROGRAM_MANDATE.json`: missão, autoridade, proibições, gates e ownership;
- `continuity/PROGRAM_QUEUE.json`: tarefas, dependências, prioridade, risco, reversibilidade, paths, acceptance command e estado;
- `continuity/PROGRAM_STATE.json`: observações, reviews, bloqueios, lanes e histórico de transição;
- `scripts/maestro_program.py`: planner e validator determinístico, sem rede obrigatória.

Os testes usam fixtures temporárias para provar o comportamento antes da migração da fila real.

## Regras de elegibilidade

Uma tarefa é elegível quando:

1. está autorizada pelo mandato;
2. suas dependências de máquina estão satisfeitas;
3. não exige gate humano ainda ausente;
4. não é destrutiva, irreversível, publicação ou produção sem autorização correspondente;
5. seus paths e recursos podem receber ownership seguro;
6. não existe bloqueio técnico específico da própria tarefa.

`machine_green_awaiting_review` satisfaz dependências para trabalho posterior reversível e não destrutivo. `ACCEPTED` continua obrigatório para release, deploy, promoção, operação destrutiva, irreversível, uso de credencial real ou consequência material explicitamente declarada.

Finding de revisão gera tarefa corretiva prioritária. Ele não bloqueia automaticamente tarefas independentes e reversíveis.

## Continuidade e parada

O planner deve retornar pelo menos:

- `eligible_tasks`;
- `blocked_tasks` com causa;
- `lanes`;
- `integration_order`;
- `parallelism_required`;
- `commit_mode`;
- `stop_allowed` e `stop_reason`.

`stop_allowed` só pode ser verdadeiro quando:

- não há tarefa elegível nem trabalho independente seguro;
- todos os fallbacks técnicos autorizados foram esgotados ou são inaplicáveis;
- o estado foi persistido e é retomável;
- a causa é conclusão, interrupção ambiental total ou gate humano válido.

Ausência de ferramenta preferida, CI não observável, primeira estratégia falha, pesquisa necessária, conflito recuperável, endpoint incompleto ou necessidade de novo teste não são gates humanos.

## Gate humano

Classes admitidas:

- `credential_required`;
- `external_authorization`;
- `financial_cost`;
- `legal_or_ethical_decision`;
- `product_consequence`;
- `irreversible_operation`;
- `destructive_production_action`.

Um gate só é válido se não houver trabalho independente elegível e se registrar condição, evidência, tentativas, fallbacks, decisão/recurso exato, estado seguro e retomada. Classe técnica ou conveniência operacional deve ser rejeitada.

## Paralelismo

Quando houver pelo menos duas tarefas elegíveis com dependências, paths e recursos separáveis:

- `parallelism_required` é verdadeiro;
- o plano cria no mínimo duas lanes;
- preparação/pesquisa/testes/patches ocorrem em ambientes isolados;
- integração, commit e push continuam seriais;
- cada lane registra `Lane-ID`, Task-ID, ownership, baseline, início, fim, output e resultado;
- a evidência deve demonstrar intervalos sobrepostos.

Sem sobreposição demonstrada, o resultado é `PARALLELISM_NOT_DEMONSTRATED`. Exceção exige `PARALLELISM_NOT_APPLICABLE` com causa objetiva.

## Commits e revisão

Cada tarefa concluída continua produzindo um commit remoto próprio por repositório afetado. Trabalho paralelo não altera a linearidade de `master`.

A revisão externa produz aceite, correção ou gate. Correções entram na fila por prioridade. O Executor não aceita o próprio trabalho, mas a espera por revisão não bloqueia automaticamente trabalho independente permitido pelo mandato.

## Acceptance command

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.acceptance.test_autonomous_program_execution -v
```

Baseline esperado ao publicar esta especificação: `RED`, porque o seam `scripts/maestro_program.py` ainda não existe. O Executor deve preservar o teste e implementar até GREEN.
