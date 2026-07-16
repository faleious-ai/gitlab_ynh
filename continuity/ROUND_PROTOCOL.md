# Protocolo de rodada de IA

## Identidade

Formato de execução: `RND-YYYYMMDD-NNN`. Uma rodada parte de um `origin/master` confirmado, executa um charter autorizado e só fica disponível para revisão quando o commit final está publicado e verificável no `origin/master` de cada repositório afetado.

Commit exclusivamente local não é persistência MAESTRO e não encerra a rodada.

## 0. ORCHESTRATE

Antes de `READY`, o orquestrador:

1. reconcilia status, handoff, decisões, evidências e HEADs remotos;
2. pergunta ao Maestro Diretor tudo que possa mudar resultado, prioridade, produto, risco, custo, acesso ou irreversibilidade;
3. decide tecnicamente questões reversíveis;
4. preenche `ACTIVE_ROUND.md` conforme `ROUND_CHARTER_CONTRACT.md`;
5. define DAG, frentes paralelas, outputs, critérios, validações, gates e plano de persistência remota;
6. não libera execução enquanto houver ambiguidade material.

## 1. START — Codex

1. confirmar repositório e branch `master`;
2. executar `git fetch origin`;
3. resolver e registrar `baseline_head = origin/master`;
4. confirmar que o HEAD local está reconciliado e que a árvore está limpa, ou tratar alterações existentes explicitamente;
5. ler `AGENTS.md`, `HANDOFF_CURRENT.md`, `STATUS.md` e `ACTIVE_ROUND.md`;
6. confirmar charter `READY` e atribuir `Round-ID`;
7. carregar contexto sob demanda;
8. registrar orientação adicional do prompt;
9. decompor o DAG e decidir o paralelismo seguro.

## 2. EXECUTE

- Executar integralmente o charter e dependências inevitáveis.
- Preferir ciclos teste-falha-correção-teste.
- Registrar fatos em arquivos/evidências, não apenas no chat.
- Decisões técnicas reversíveis podem ser tomadas autonomamente.
- Não promover plano, hipótese ou output parcial a concluído.
- Não encerrar para apresentar progresso.
- Teste falho, pesquisa longa, primeira estratégia malsucedida e volume de trabalho não são bloqueios.

## 3. PARALLELIZE

Quando o DAG permitir:

1. criar frentes independentes com ownership de paths/outputs;
2. fornecer contexto mínimo a cada subagente;
3. proibir commits, push e expansão de escopo pelos subagentes;
4. exigir retorno com fatos, alterações, validações, desconhecidos e riscos;
5. continuar frentes independentes quando outra falhar;
6. integrar, revisar e validar centralmente.

Arquivos canônicos compartilhados, decisões arquiteturais, integração final, commit e push permanecem sequenciais sob o executor principal.

## 4. VALIDATE

Aplicar validação proporcional:

- documentação: links, IDs, estados, cobertura e contradições;
- pacote: lint, testes YunoHost, sources e lifecycle aplicável;
- updater: fixtures, hashes, assets, versões, falhas, determinismo e idempotência;
- MCP: schema, autenticação, paginação, rate limit, retry, idempotência e isolamento destrutivo;
- cross-repo: decisões, versões, evidências e mesmo `Round-ID`.

Toda alegação de conclusão aponta para evidência ou permanece `UNVERIFIED`.

## 5. BLOCKER SWEEP

Antes de parar por bloqueio:

1. identificar quais nós do DAG realmente dependem do gate;
2. concluir todos os nós independentes;
3. tentar alternativas técnicas razoáveis;
4. deixar estado seguro e verificável;
5. registrar condição, evidência, tentativas, alternativas, decisão humana exata e grafo restante.

Bloqueio humano é decisão, credencial de produto, autorização, irreversibilidade ou consequência prática. Limite de sessão, ferramenta ou push é interrupção ambiental/sincronização, não conclusão.

## 6. PERSIST LOCAL

No mesmo fechamento lógico:

1. atualizar `STATUS.md`;
2. substituir `HANDOFF_CURRENT.md`;
3. atualizar o estado de `ACTIVE_ROUND.md`;
4. atualizar decisões/ADRs quando necessário;
5. adicionar round record append-only;
6. atualizar `EVIDENCE_INDEX.md`;
7. executar `git fetch origin` e reconciliar novamente o HEAD;
8. revisar diff, segredos, ruído e claims;
9. repetir validações impactadas;
10. criar exatamente um commit local da rodada por repositório.

Após o commit local, o estado máximo permitido é `LOCAL_COMPLETE_AWAITING_SYNC`.

## 7. REMOTE SYNC

Para cada repositório afetado:

1. executar `git fetch origin`;
2. verificar `git rev-list --left-right --count origin/master...HEAD`;
3. quando o resultado for `0 1`, executar `git push origin master`;
4. se `origin/master` tiver avançado, não force: rebasear ou recriar somente o commit ainda não publicado sobre o novo `origin/master`, resolver conflitos, repetir checks impactados e preservar um único commit final da rodada;
5. se houver credencial ausente, rejeição não reconciliável ou indisponibilidade, registrar `REMOTE_SYNC_BLOCKED` com comando, erro, divergência, tentativas e ação necessária;
6. após o push, executar novo `git fetch origin`;
7. confirmar `git rev-parse HEAD == git rev-parse origin/master`;
8. confirmar que o SHA completo é recuperável pelo GitHub e que os arquivos/evidências citados existem no remoto;
9. em trabalho cross-repo, repetir para todos os repositórios antes de declarar revisão disponível.

Nunca usar force push. Nunca considerar `git commit` suficiente sem `git push` e verificação remota.

## 8. ESTADOS DE SAÍDA DO EXECUTOR

- `LOCAL_COMPLETE_AWAITING_SYNC`: tarefas e checks concluídos, commit apenas local.
- `REMOTE_SYNC_BLOCKED`: resultado local seguro, mas publicação remota falhou ou divergiu.
- `BLOCKED_HUMAN`: todo trabalho independente e toda persistência possível foram concluídos, restando gate humano real.
- `EXECUTED_AWAITING_REVIEW`: commit publicado em `origin/master` de todos os repositórios afetados, HEADs coincidentes, árvore limpa, evidências remotas e pacote de revisão completo.

O Codex não marca o próprio trabalho `ACCEPTED`.

## 9. PACOTE REMOTO DE REVISÃO

Entregar:

- nomes dos repositórios;
- SHAs completos publicados;
- `Round-ID` e `Charter-ID`;
- matriz tarefa → output → evidência;
- comandos e resultados de validação;
- paths e URLs do GitHub, nunca links locais como `C:/...`;
- riscos residuais e gates;
- confirmação de `HEAD == origin/master` e árvore limpa.

## 10. REVIEW

O orquestrador aplica `REVIEW_PROTOCOL.md` somente sobre material remoto e registra `ACCEPTED`, `CORRECTION_REQUIRED`, `HUMAN_GATE` ou `REJECTED_UNSAFE`. Após gate humano, revisa o charter e libera nova rodada vinculada ao mesmo objetivo quando aplicável.

## Concorrência externa

Se `origin/master` mudar durante a rodada: não force. Leia os commits novos, reconcilie contratos, rebaseie ou recrie apenas o commit local ainda não publicado quando seguro, repita checks impactados e registre conflito se incompatível.