# Modelo de orquestração e execução

## Papéis

- **Maestro Diretor humano:** missão, prioridade, consequências práticas, gates éticos, custos relevantes, acesso privilegiado e operações irreversíveis.
- **ChatGPT — orquestrador e revisor externo:** reconcilia estado remoto, resolve perguntas materiais, especifica rodadas/tarefas, revisa cada commit e o resultado integrado e decide aceite, correção ou gate humano.
- **Codex — executor principal:** executa integralmente o charter `READY`, coordena subagentes, integra, valida, cria um commit por tarefa, publica e prepara evidências. Não aprova o próprio resultado.
- **Subagentes:** frentes independentes sem commit, push, integração final, edição concorrente ou expansão de escopo.
- **Revisores internos:** contextos separados nos eixos Spec/Charter e Engineering/Security/Lifecycle antes de cada commit.

## Unidades

- rodada: autorização, baseline, escopo, DAG, gates e veredito;
- tarefa: resultado atômico, seam, claims, TDD, commit, sincronização e rollback;
- commit: versão remota e reversível da tarefa;
- evidência: prova de claim em nível estrutural, local, CI ou lifecycle.

## Invocação

`Leia AGENTS.md e continue` executa o charter ativo, tarefa por tarefa, e só para após concluir tudo que não esteja bloqueado por decisão humana real ou interrupção ambiental persistida.

## Fluxo

```text
Maestro Diretor
  → ChatGPT/orquestrador
  → charter READY + Task-IDs
  → Codex/subagentes
  → RED/GREEN + gates + revisão interna
  → commit remoto por tarefa
  → pacote baseline...round_head
  → ChatGPT/revisor externo
  → ACCEPTED | CORRECTION_REQUIRED | HUMAN_GATE | REJECTED_UNSAFE
```

## Autonomia

Orquestrador e executor decidem escolhas técnicas reversíveis e backprop técnico. O humano é acionado apenas quando a escolha altera missão, produto, compatibilidade prometida, custo relevante, risco aceito, privilégio, publicação ou irreversibilidade.

## Revisão

A autoria não valida a própria conclusão. O executor realiza checks e revisão interna, mas termina em `EXECUTED_AWAITING_REVIEW`. O ChatGPT revisa material remoto, cada Task-ID e o intervalo integrado. Claims sem prova permanecem unverified.

## Bloqueio

Em gate humano, o executor conclui tarefas independentes, publica tudo que for seguro e registra condição, tentativas, alternativas, decisão exata e grafo restante. Falha de push é `TASK_REMOTE_SYNC_BLOCKED`, não gate de produto.

## Autoridade cross-repo

`gitlab_ynh` coordena o programa e decisões transversais. `gitlab-runner_ynh` mantém autoridade sobre Runner, helper images, tokens, Docker, updater, skills de execução e lifecycle. Futuro `gitlab-mcp` manterá a implementação MCP quando criado.
