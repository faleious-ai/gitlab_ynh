# Protocolo de rodada de IA

## Identidade

Formato de execução: `RND-YYYYMMDD-NNN`. Uma rodada parte de um HEAD confirmado, executa um charter autorizado e termina por commit em `master` ou por bloqueio persistido em estado seguro.

## 0. ORCHESTRATE

Antes de `READY`, o orquestrador:

1. reconcilia status, handoff, decisões, evidências e HEADs;
2. pergunta ao Maestro Diretor tudo que possa mudar resultado, prioridade, produto, risco, custo, acesso ou irreversibilidade;
3. decide tecnicamente questões reversíveis;
4. preenche `ACTIVE_ROUND.md` conforme `ROUND_CHARTER_CONTRACT.md`;
5. define DAG, frentes paralelas, outputs, critérios, validações e gates;
6. não libera execução enquanto houver ambiguidade material.

## 1. START — Codex

1. confirmar repositório e branch `master`;
2. resolver HEAD local/remoto e registrar `baseline_head`;
3. confirmar árvore limpa ou reconciliar alterações existentes;
4. ler `AGENTS.md`, `HANDOFF_CURRENT.md`, `STATUS.md` e `ACTIVE_ROUND.md`;
5. confirmar charter `READY` e atribuir `Round-ID`;
6. carregar contexto sob demanda;
7. registrar orientação adicional do prompt;
8. decompor o DAG e decidir o paralelismo seguro.

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
3. proibir commits e expansão de escopo pelos subagentes;
4. exigir retorno com fatos, alterações, validações, desconhecidos e riscos;
5. continuar frentes independentes quando outra falhar;
6. integrar, revisar e validar centralmente.

Arquivos canônicos compartilhados, decisões arquiteturais, integração final e commit permanecem sequenciais sob o executor principal.

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

Bloqueio humano é decisão/credencial/autorização/irreversibilidade/consequência prática. Limite externo de sessão ou ferramenta é interrupção ambiental, não conclusão.

## 6. PERSIST

No mesmo fechamento lógico:

1. atualizar `STATUS.md`;
2. substituir `HANDOFF_CURRENT.md`;
3. atualizar o estado de `ACTIVE_ROUND.md`;
4. atualizar decisões/ADRs quando necessário;
5. adicionar round record append-only;
6. atualizar `EVIDENCE_INDEX.md`;
7. reconciliar novamente HEAD e repetir validações impactadas;
8. revisar diff, segredos, ruído e claims.

## 7. COMMIT

Política normativa para rodadas futuras: exatamente um commit por rodada e repositório.

```text
<type>(<scope>): <resultado observável>

Round-ID: RND-YYYYMMDD-NNN
Charter-ID: CHR-...
Work-Package: WP-XX
Evidence: EVD-...
```

Trabalho cross-repo repete o mesmo `Round-ID`.

## 8. EXECUTOR END

O Codex termina somente quando:

- todas as tarefas não bloqueadas foram concluídas;
- commit está em `master` e árvore limpa;
- status, handoff, active round e evidência correspondem ao resultado;
- pacote de revisão está completo;
- estado é `EXECUTED_AWAITING_REVIEW` ou `BLOCKED_HUMAN`.

O Codex não marca o próprio trabalho `ACCEPTED`.

## 9. REVIEW

O orquestrador aplica `REVIEW_PROTOCOL.md` e registra `ACCEPTED`, `CORRECTION_REQUIRED`, `HUMAN_GATE` ou `REJECTED_UNSAFE`. Após gate humano, revisa o charter e libera nova rodada vinculada ao mesmo objetivo quando aplicável.

## Concorrência externa

Se `master` mudar durante a rodada: não force; leia commits novos, reconcilie contratos, repita checks impactados e registre conflito se incompatível.
