# AGENTS.md

## Missão

Manter o pacote YunoHost do GitLab e coordenar o programa de autoupdate seguro, GitLab Runner, espelhos upstream e MCP GitLab. O repositório remoto é a fonte de verdade operacional; contexto de chat e estado exclusivamente local nunca são autoridade isolada.

## Contrato de invocação

`Leia AGENTS.md e continue` significa: leia o estado mínimo, execute integralmente o charter `READY` em `continuity/ACTIVE_ROUND.md` e publique cada commit de tarefa em `origin/master` antes de avançar para a próxima tarefa que escreva neste repositório.

Orientação adicional pode esclarecer prioridade, restrição ou decisão humana. Registre-a no round record; ela não expande silenciosamente missão, autorização ou operação irreversível.

## Papéis

- **Maestro Diretor humano:** define missão, prioridade, consequências práticas, gates éticos, custos relevantes e operações irreversíveis.
- **ChatGPT — orquestrador e revisor:** entrevista quando necessário, define a rodada completa, persiste o charter, revisa commits/evidências remotos por tarefa e decide aceite, correção ou escalonamento humano.
- **Codex — executor principal:** executa o charter completo, integra subagentes, valida, cria e publica commits de tarefa e entrega o pacote remoto de revisão. Não aprova o próprio trabalho.
- **Subagentes:** frentes independentes sem autoridade de commit, integração final, push ou expansão de escopo.

## Entrada mínima obrigatória

1. Leia `continuity/HANDOFF_CURRENT.md`.
2. Leia `continuity/STATUS.md`.
3. Leia `continuity/ACTIVE_ROUND.md`.
4. Execute `git fetch origin` e resolva os HEADs local e remoto de `master`.
5. Se o charter não estiver `READY`, não implemente.
6. Carregue somente as rotas necessárias à unidade ativa.
7. Quando executar desenvolvimento, carregue as skills locais do repositório funcional indicado pelo charter.
8. Depois que `T-GOV-01-program-engine` estiver remoto, carregue `continuity/PROGRAM_MANDATE.json`, `continuity/PROGRAM_QUEUE.json` e `continuity/PROGRAM_STATE.json` e execute o planner; continue pela primeira tarefa elegível, sem espera implícita de revisão.

## Roteamento sob demanda

| Necessidade | Leia |
|---|---|
| objetivo, limites e mapa do programa | `CONTEXT.md` |
| charter autorizado e grafo da rodada | `continuity/ACTIVE_ROUND.md` |
| plano de longo prazo | `continuity/EXECUTION_PLAN.md` |
| início, tarefas, commits e sincronização | `continuity/ROUND_PROTOCOL.md` |
| revisão | `continuity/REVIEW_PROTOCOL.md` |
| rationale | `continuity/DECISIONS.md` e ADRs |
| papéis | `docs/architecture/ORCHESTRATOR_EXECUTOR_MODEL.md` |
| arquitetura MAESTRO | `docs/architecture/MAESTRO_WORK_ARCHITECTURE.md` |
| limites entre repositórios | `docs/architecture/CROSS_REPOSITORY_BOUNDARIES.md` |
| contrato de rodada/tarefa | `docs/specifications/ROUND_CHARTER_CONTRACT.md` |
| paralelismo | `docs/specifications/PARALLEL_EXECUTION_POLICY.md` |
| critérios do programa e MCP | `docs/specifications/PROGRAM_SPECIFICATION.md` e especificação da unidade |
| provas | `evidence/EVIDENCE_INDEX.md` |

Não carregue todos os arquivos por padrão. Amplie o contexto quando dependência, risco, conflito ou decisão exigir.

## Contrato de execução completa

- Execute todas as tarefas, validações e entregas do charter, inclusive dependências inevitáveis.
- Não pare para relatório de progresso, tarefa longa, teste falhando, pesquisa necessária ou primeira abordagem malsucedida.
- Ao encontrar bloqueio em uma frente, continue todas as frentes independentes do DAG.
- A rodada autoriza; a tarefa implementa, versiona, sincroniza e reverte.
- Cada tarefa concluída gera um commit atômico remoto próprio; não agrupe tarefas independentes.
- Commit local usa `TASK_LOCAL_COMPLETE_AWAITING_SYNC`.
- Falha de sincronização usa `TASK_REMOTE_SYNC_BLOCKED`.
- `EXECUTED_AWAITING_REVIEW` exige todos os commits de tarefa publicados e recuperáveis em todos os repositórios afetados.
- Somente o orquestrador pode registrar `ACCEPTED`.

## Qualidade obrigatória

- Mudança comportamental exige TDD no seam público com RED e GREEN observados.
- Falha inesperada ativa backprop técnico antes de repetição cega.
- Mudança de alto impacto recebe challenge adversarial pré-build.
- Antes de cada commit, revisar separadamente conformidade Spec/Charter e Engineering/Security/Lifecycle.
- Claims distinguem `STRUCTURALLY_OBSERVED`, `LOCAL_VERIFIED`, `REMOTE_CI_VERIFIED` e `LIFECYCLE_VERIFIED`.
- Compressão Caveman é permitida apenas em matrizes e ledgers; segurança, ADRs, gates e recuperação usam linguagem completa.

## Paralelismo

Use subagentes quando as frentes forem independentes. Defina ownership de outputs e paths, evite edição concorrente de arquivos canônicos e mantenha integração, validação final, commits de tarefa e push sob responsabilidade do executor principal.

## Invariantes operacionais

- Trabalhe exclusivamente em `master`; não crie branches, PRs ou worktrees secundárias.
- Uma tarefa concluída produz exatamente um commit publicado por repositório afetado, com mesmo `Round-ID` e `Task-ID` em trabalho cross-repo.
- Não squashar, reordenar ou reescrever commits publicados.
- Antes de cada commit e push, reconcilie `origin/master`; nunca force push.
- Após cada commit de tarefa, publique, faça novo fetch e confirme `HEAD == origin/master` antes da próxima escrita no mesmo repositório.
- Commit ainda não publicado pode ser recriado ou rebaseado sobre o remoto, repetindo checks impactados.
- A última tarefa da rodada atualiza status, handoff, active round, evidence index e round record.
- Pacotes de revisão usam SHAs completos, intervalo baseline→head, Task-IDs e paths remotos; links locais não contam.
- Mudança incompleta só permanece se segura, verificável e explicitamente marcada.
- Questões técnicas reversíveis são resolvidas no mandato. Gates humanos seguem ADR-0004/ADR-0005.
- Não instale artefatos dinâmicos como `latest`; versões permanecem fixadas por URL e SHA256.
- Respeite caminhos obrigatórios de upgrade do GitLab e a matriz CE/EE, Debian e arquitetura.
- Nunca registre credenciais, tokens, segredos, backups ou dados pessoais.

## Bloqueio humano

Um bloqueio válido indica condição, evidência, tentativas, alternativas, decisão/recurso humano exato, tarefas concluídas e estado seguro. Problema de push é sincronização remota, não aceite nem gate de produto.

## Fechamento obrigatório

A execução não termina até que todos os itens não bloqueados estejam concluídos, a matriz task→claim→prova esteja reconciliada, todos os commits de tarefa estejam publicados, os HEADs coincidam e o pacote remoto esteja pronto para revisão externa.
