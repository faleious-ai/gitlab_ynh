# Protocolo de rodada de IA

## Identidade

Formato: `RND-YYYYMMDD-NNN`.

Uma rodada é uma unidade de execução iniciada a partir de um HEAD confirmado e encerrada por um único commit atômico em `master`.

## 1. START

1. confirmar repositório e branch `master`;
2. resolver HEAD local/remoto e registrar `baseline_head`;
3. confirmar árvore limpa ou reconciliar alterações existentes;
4. ler `AGENTS.md`, `HANDOFF_CURRENT.md` e `STATUS.md`;
5. identificar a unidade ativa e carregar contexto sob demanda;
6. declarar escopo, fora de escopo, critérios de aceite, riscos e validações;
7. não iniciar se houver conflito de autoridade ou segredo necessário ausente.

## 2. EXECUTE

- Trabalhar somente na unidade autorizada e dependências inevitáveis.
- Preferir ciclos teste-falha-correção-teste quando houver comportamento executável.
- Registrar descobertas factuais em documentos de auditoria ou evidência, não apenas no chat.
- Decisões técnicas reversíveis podem ser tomadas autonomamente.
- Ao detectar drift, reler somente a fonte canônica afetada.
- Não promover plano, hipótese ou output parcial a “concluído”.

## 3. VALIDATE

Aplicar validação proporcional:

- documentação: consistência de links, IDs, estados e ausência de contradições;
- pacote: lint, testes YunoHost relevantes, integridade de sources e lifecycle aplicável;
- updater: fixtures, hashes, assets, versões, erros e idempotência;
- MCP: schema, autenticação, paginação, rate limit, retry, idempotência, erros e isolamento destrutivo;
- cross-repo: mesma decisão, versão e Round-ID nos repositórios afetados.

Toda alegação de conclusão deve apontar para evidência reproduzível ou ser marcada como não verificada.

## 4. PERSIST

Antes do commit:

1. atualizar `continuity/STATUS.md` com estado factual;
2. substituir `continuity/HANDOFF_CURRENT.md` pelo próximo ponto de entrada;
3. atualizar `continuity/DECISIONS.md` e ADRs quando necessário;
4. adicionar registro append-only em `continuity/rounds/`;
5. atualizar `evidence/EVIDENCE_INDEX.md`;
6. reconciliar o HEAD de `master`; se mudou, integrar sem force push e repetir validações impactadas;
7. revisar diff inteiro e remover segredos, ruído e afirmações não comprovadas.

## 5. COMMIT

Exatamente um commit por rodada neste repositório.

Formato recomendado:

```text
<type>(<scope>): <resultado observável>

Round-ID: RND-YYYYMMDD-NNN
Work-Package: WP-XX
Evidence: EVD-...
```

Tipos preferidos: `docs`, `test`, `fix`, `feat`, `refactor`, `chore`, `ci`.

Não usar commit genérico como `update`, `changes` ou `checkpoint` sem descrição observável.

## 6. END

A rodada termina somente quando:

- commit está em `master`;
- working tree está limpa;
- status e handoff correspondem ao commit;
- evidência está indexada;
- próxima unidade ou bloqueio está explícito.

O SHA resultante é obtido pelo commit que contém o arquivo de rodada. O campo `result_commit: SELF` evita um segundo commit apenas para registrar o próprio SHA.

## Concorrência

Se outro agente alterar `master` durante a rodada:

- não sobrescrever nem forçar;
- ler os commits novos;
- reconciliar contratos e documentos canônicos;
- repetir validações relevantes;
- abortar e registrar conflito se as mudanças forem incompatíveis.

## Bloqueio

Um bloqueio válido deve conter:

- condição exata;
- evidência;
- tentativas feitas;
- alternativas descartadas e rationale;
- decisão ou recurso humano necessário;
- estado seguro deixado no repositório.

Não é bloqueio: tarefa longa, necessidade de pesquisar, teste falhar ou primeira abordagem não funcionar.