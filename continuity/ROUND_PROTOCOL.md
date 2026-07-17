# Protocolo de rodada de IA

Identificadores: `RND-YYYYMMDD-NNN` e `T-<NN>-<slug>`.

A rodada é a unidade de autorização, baseline, escopo e veredito. A tarefa é a unidade de implementação, commit, sincronização e reversão. Commit exclusivamente local não é persistência MAESTRO.

## 0. ORCHESTRATE

Antes de `READY`, o orquestrador:

1. reconcilia status, handoff, decisões, evidências e HEADs remotos;
2. pergunta ao Maestro Diretor somente o que muda resultado, prioridade, produto, risco, custo, acesso ou irreversibilidade;
3. decide questões técnicas reversíveis;
4. define tarefas com `Task-ID`, dependências, seam, claims/invariantes, paths, TDD, gates, review e rollback;
5. define DAG, paralelismo seguro e commits cross-repo;
6. não libera execução enquanto houver ambiguidade material.

## 1. START — Codex

1. confirmar repositório e `master`;
2. executar `git fetch origin`;
3. registrar `baseline_head = origin/master`;
4. confirmar HEAD reconciliado e árvore limpa;
5. ler `AGENTS.md`, `HANDOFF_CURRENT.md`, `STATUS.md` e `ACTIVE_ROUND.md`;
6. confirmar charter `READY`, atribuir `Round-ID` e registrar orientação adicional;
7. decompor o DAG em tarefas e frentes com ownership.

## Fila canônica após o motor

Quando `T-GOV-01-program-engine` estiver remoto e GREEN, a continuidade executável passa a ser a combinação de `PROGRAM_MANDATE.json`, `PROGRAM_QUEUE.json` e `PROGRAM_STATE.json`. O comando de retomada é:

```text
python3 scripts/maestro_program.py plan --mandate continuity/PROGRAM_MANDATE.json --queue continuity/PROGRAM_QUEUE.json --state continuity/PROGRAM_STATE.json
```

O resultado `eligible_tasks` orienta a próxima tarefa. `machine_green_awaiting_review` satisfaz dependências reversíveis; gate, release, deploy, promoção, produção e destruição continuam protegidos. A fila e o estado são atualizados por tarefa, com integração, commit e push seriais.

## 2. PRE-BUILD CHALLENGE

Mudança de alto impacto passa por tentativa de refutação antes do primeiro edit: goal real, seams, invariantes ausentes, interface drift, lifecycle, segurança, rollback e fontes externas. Lacunas técnicas reversíveis são corrigidas; decisão material vira gate humano. Registrar `GO` ou `NO_GO` com evidência.

## 3. EXECUTE — POR TAREFA

Para cada tarefa:

1. carregar apenas contexto e skills aplicáveis;
2. confirmar seam público e contrato de verificação;
3. usar RED→GREEN para qualquer mudança comportamental;
4. implementar o mínimo necessário;
5. executar gates do mais barato ao mais caro;
6. em falha inesperada, classificar e executar backprop antes de retry cego;
7. manter matriz claim → mecanismo → comando → resultado → estado de evidência;
8. continuar tarefas independentes quando uma frente bloquear.

## 4. BACKPROP

Classificações mínimas: `IMPLEMENTATION_BUG`, `MISSING_CRITERION`, `INCOMPLETE_CRITERION`, `WRONG_CRITERION`, `MISSING_REQUIREMENT`, `ENVIRONMENTAL_LIMIT`, `EXTERNAL_DEPENDENCY`.

O executor pode ajustar autonomamente critério, invariante, teste e memória quando a consequência é técnica e reversível. Alteração de produto, comportamento externo, custo, privilégio, risco ou irreversibilidade exige decisão do Maestro Diretor.

## 5. PARALLELIZE

Frentes independentes recebem paths e outputs exclusivos. Subagentes não fazem commit, push, expansão de escopo ou edição concorrente de arquivos canônicos. O executor integra uma tarefa por vez, valida e publica.

## 6. INTERNAL REVIEW

Antes de cada commit, executar duas revisões independentes:

- **Spec/Charter:** requisitos ausentes/parciais, scope creep, interfaces e claims sem prova;
- **Engineering:** bugs, segurança, lifecycle, compatibilidade, simplicidade, falhas negativas e reversibilidade.

P0/P1 bloqueiam. P2/P3 são corrigidos ou justificados no pacote remoto.

## 7. TASK COMMIT

1. executar `git fetch origin` e reconciliar apenas trabalho ainda não publicado;
2. revisar diff, segredos, ruído, paths e claims;
3. repetir checks impactados;
4. criar exatamente um commit atômico por tarefa e repositório afetado;
5. mensagem: `RND-<id> T-<id>: <resultado>`;
6. não incluir outra tarefa independente;
7. não criar commit separado apenas para RED; registrar RED de forma versionada e entregar teste+fix no commit coerente;
8. não squashar ou reescrever commit publicado.

Estado local: `TASK_LOCAL_COMPLETE_AWAITING_SYNC`.

## 8. TASK REMOTE SYNC

1. executar `git fetch origin`;
2. confirmar fast-forward seguro;
3. executar `git push origin master` sem force;
4. fazer novo fetch e confirmar `HEAD == origin/master`;
5. confirmar SHA completo recuperável e outputs remotos;
6. marcar `TASK_REMOTE_VERIFIED` antes da próxima tarefa que escreva nesse repositório.

Falha produz `TASK_REMOTE_SYNC_BLOCKED`; não empilhar novos commits no mesmo repositório. Trabalho cross-repo usa o mesmo `Round-ID` e `Task-ID` e só fecha após todos os commits correspondentes estarem remotos.

## 9. CONVERGENCE

Monitorar claims demonstrados, gates, findings P0–P3, tarefas, falhas/backprop e estabilidade do diff como sinal secundário. Oscilação ou repetição indica problema de spec, validação ou ownership; não aumente iterações sem corrigir a causa.

## 10. ROUND CLOSE

A última tarefa da rodada reconcilia `STATUS`, `HANDOFF_CURRENT`, `ACTIVE_ROUND`, decisões, evidence index e round record.

`EXECUTED_AWAITING_REVIEW` exige todos os commits de tarefa publicados entre `baseline_head` e `round_head`, HEADs coincidentes, árvores limpas, matriz task→commit→claim→evidência e pacote remoto completo.

O Codex não marca `ACCEPTED`.

## 11. REVIEW

O ChatGPT revisa cada commit de tarefa e o intervalo integrado `baseline_head...round_head`. Persiste aceite, correção, gate humano ou rejeição insegura em tarefas/commits próprios de orquestração.
