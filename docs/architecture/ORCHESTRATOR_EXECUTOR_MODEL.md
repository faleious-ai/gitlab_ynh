# Modelo de orquestração e execução

## Papéis

### Maestro Diretor humano

O usuário define missão, prioridades, consequências práticas aceitáveis, limites éticos, custos relevantes, operações irreversíveis e demais gates humanos.

### Orquestrador e revisor

O ChatGPT atua como orquestrador e revisor do trabalho realizado via repositório. Antes de liberar uma rodada:

1. reconcilia estado, decisões, evidências e bloqueios;
2. pergunta ao Maestro Diretor tudo que possa alterar resultado, produto, risco, custo, irreversibilidade ou prioridade;
3. resolve autonomamente questões técnicas reversíveis;
4. produz ou revisa `continuity/ACTIVE_ROUND.md` com escopo completo, critérios, grafo de dependências, paralelismo, validações e gates;
5. após a execução, revisa commits, diff, evidências, critérios e riscos residuais;
6. aceita o resultado, define rodada corretiva ou leva bloqueio humano ao Maestro Diretor.

### Executor principal

O Codex é o executor principal. A instrução humana `Leia AGENTS.md e continue` significa executar integralmente o contrato `READY` em `continuity/ACTIVE_ROUND.md`.

O Codex não redefine missão nem encerra por conveniência. Ele trabalha até:

- concluir todas as tarefas e critérios da rodada; ou
- concluir tudo que permanece executável e persistir um bloqueio humano válido para o restante.

### Subagentes

Subagentes aceleram frentes independentes. Eles não possuem autoridade de integração nem de commit. O executor principal:

- decompõe o grafo;
- atribui escopos de arquivos e outputs sem sobreposição;
- recebe resultados estruturados;
- verifica evidências;
- reconcilia conflitos;
- integra e valida o conjunto.

## Fluxo

`Maestro Diretor -> Orquestrador -> ACTIVE_ROUND -> Codex/subagentes -> commit/evidência -> Orquestrador -> aceite, correção ou gate humano`.

## Fonte de autoridade

- missão e gates: Maestro Diretor;
- contrato da rodada: `ACTIVE_ROUND.md` preparado pelo orquestrador;
- execução factual: commits, testes e evidências;
- aceite: revisão do orquestrador;
- chat sem persistência não substitui arquivos canônicos.

## Continuidade após bloqueio humano

Quando existir gate humano, o Codex termina primeiro todas as tarefas independentes. Depois deixa estado seguro, evidência e grafo restante. O usuário e o orquestrador resolvem o gate. A retomada usa nova revisão do charter e novo `Round-ID`, vinculados ao mesmo `Charter-ID` quando o objetivo permanece o mesmo.
