# Rodada ativa

Charter-ID: `CHR-WP02-001`  
Estado: `READY`  
Preparado em: 2026-07-16  
Orquestrador: ChatGPT com o Maestro Diretor  
Executor principal: Codex  
Work Package: `WP-02 — Segurança e fundação determinística do autoupdate do Runner`

## Autorização de entrada

O prompt `Leia AGENTS.md e continue` autoriza a execução integral deste charter. O executor deve atribuir um novo `Round-ID` no START e usar o mesmo identificador nos dois repositórios quando ambos forem atualizados.

## Resultado da revisão anterior

`CHR-WP01-001`, executado em `RND-20260716-003`, foi `ACCEPTED` pelo orquestrador. A revisão está em `continuity/reviews/REV-RND-20260716-003.md`.

## Objetivo

Eliminar o risco de credencial persistida na árvore atual do Runner, tornar a ação administrativa `register` coerente e testável e implementar a fundação determinística do atualizador Runner + helper images, sem promover uma nova versão de produção nem executar registro real.

## Repositório primário

`faleious-ai/gitlab-runner_ynh`.

Este repositório coordenador deve receber somente a síntese cross-repo, decisões duráveis aplicáveis ao programa, estado, handoff, evidência e round record com o mesmo `Round-ID`.

## Escopo completo

### WP-02S — Remediação de segurança

- remover da árvore atual qualquer literal com aparência de credencial em fixtures;
- substituir por mecanismo de teste que não persista segredo;
- adicionar verificação automatizada contra credenciais e outputs sensíveis;
- garantir que testes, logs e relatórios nunca reproduzam o valor histórico;
- registrar que revogação/expiração do valor histórico é gate humano externo.

### WP-02R — Registro administrativo

- pesquisar o contrato atual de actions do YunoHost;
- reparar ou remover justificadamente a ação `register` hoje apontada para target inexistente;
- preferir uma única implementação reutilizada por install, restore e action;
- validar cardinalidade de URL/token/imagem e falhar de forma segura;
- impedir exposição de token em logs e reduzir exposição em argumentos de processo quando tecnicamente viável;
- cobrir comportamento com testes sem usar GitLab real.

### WP-02A/B/C — Fundação do atualizador

- escolher e registrar fonte oficial de release e proveniência;
- resolver atomicamente binários amd64, arm64, armhf e helper images da mesma versão;
- obter ou recalcular SHA256 e falhar se qualquer célula estiver ausente ou incompatível;
- implementar geração determinística, idempotente e com staging atômico;
- limitar escrita aos campos autorizados do manifest e documentação gerada;
- oferecer modo somente verificação/dry-run com relatório machine-readable;
- usar fixtures offline nos testes;
- não modificar a versão declarada do pacote nesta rodada.

### Assurance e CI

- testes positivos e negativos para release, assets, helper images, hashes, rede, escrita parcial, determinismo e idempotência;
- teste estrutural para toda action declarar target existente;
- teste de redaction/ausência de segredo;
- workflow de CI compatível com `master`, inicialmente sem mutação automática do repositório;
- executar todos os checks disponíveis e marcar explicitamente limitações ambientais.

## DAG paralelo

### Onda 1

- Frente A: fixture segura, secret scan e política de redaction.
- Frente B: contrato YunoHost da action e implementação compartilhada de registro.
- Frente C: pesquisa da fonte oficial, schema de fixture e ADR de proveniência.
- Frente D: resolver/generator Runner + helper images.
- Frente E: testes, CI e harness de falha fechada.

Subagentes têm ownership exclusivo de outputs e não fazem commit. Arquivos canônicos compartilhados são integrados somente pelo executor principal.

### Gate de integração

O Codex reconcilia interfaces, elimina duplicação, verifica que nenhum segredo entrou no diff e executa a suíte completa.

### Onda 2

- integração do updater com manifest em dry-run;
- documentação operacional;
- relatório de candidata sem promoção;
- atualização cross-repo;
- pacote de evidência e continuidade.

## Fora de escopo

- usar o valor histórico da credencial;
- consultar a validade do valor por tentativa de autenticação;
- registrar Runner real ou atuar em produção;
- promover versão candidata no manifest;
- publicar release;
- reescrever histórico ou usar force push;
- criar branch, PR, mirror ou alterar ruleset;
- executar `unregister --all-runners` fora de ambiente efêmero.

## Gate humano não bloqueante durante a execução

`HG-RUN-SEC-01`: confirmar revogação, rotação ou expiração do valor histórico no projeto GitLab usado pelo package_check. O Codex não executa essa ação nem usa o valor. Deve concluir todas as tarefas técnicas independentes antes de declarar `BLOCKED_HUMAN` caso o gate permaneça aberto.

## Outputs obrigatórios no Runner

- implementação do updater e registro seguro;
- fixtures e testes;
- CI de validação sem mutação automática;
- ADR de fonte/proveniência;
- documentação de segurança e operação;
- `STATUS`, `HANDOFF_CURRENT`, `ACTIVE_ROUND`, `EVIDENCE_INDEX` e round record.

## Output obrigatório neste coordenador

- síntese de execução, riscos, decisões e evidências do Runner;
- estado do gate humano;
- próximo passo do programa.

## Definition of Done

- o literal credential-like não existe na árvore atual nem nos novos outputs;
- secret scan e testes impedem recorrência;
- a action `register` é executável e testada ou foi removida com rationale e contratos atualizados;
- resolver/generator é determinístico, idempotente, atômico e falha fechado;
- Runner e helper images são sempre resolvidos como conjunto da mesma versão;
- nenhuma promoção de versão ocorreu;
- CI/checks locais disponíveis passaram ou têm limitação explícita;
- todos os itens não bloqueados foram concluídos;
- um commit em `master` por repositório afetado, mesmo `Round-ID`;
- estado final `EXECUTED_AWAITING_REVIEW`, ou `BLOCKED_HUMAN` somente após completar todo o restante.

## Pacote de revisão

Entregar commits, matriz tarefa → output → evidência, comandos e resultados, cobertura de testes, diff de segurança, candidata observada sem promoção, riscos residuais e estado de `HG-RUN-SEC-01`. Não declarar `ACCEPTED`.