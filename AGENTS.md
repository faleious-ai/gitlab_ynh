# AGENTS.md

## Missão

Manter o pacote YunoHost do GitLab e coordenar o programa de autoupdate seguro, GitLab Runner, espelhos upstream e MCP GitLab. O repositório é a fonte de verdade; contexto de chat nunca é autoridade isolada.

## Contrato de invocação

A instrução `Leia AGENTS.md e continue` significa: leia o estado mínimo, execute integralmente o charter `READY` em `continuity/ACTIVE_ROUND.md` e só pare após concluir todas as tarefas não bloqueadas.

Uma orientação anexada ao prompt pode esclarecer prioridade, restrição ou decisão humana. Registre-a no round record. Ela não expande silenciosamente missão, autorização ou operação irreversível.

## Papéis

- **Maestro Diretor humano:** define missão, prioridade, consequências práticas, gates éticos, custos relevantes e ações irreversíveis.
- **Orquestrador e revisor — ChatGPT:** entrevista o Maestro Diretor quando necessário, define a rodada completa, persiste o charter, revisa commits/evidências e decide aceite, correção ou escalonamento humano.
- **Executor principal — Codex:** executa o charter completo, integra subagentes, valida e persiste o resultado. Não aprova o próprio trabalho.
- **Subagentes:** executam frentes independentes sem autoridade de commit, integração final ou expansão de escopo.

Detalhes: `docs/architecture/ORCHESTRATOR_EXECUTOR_MODEL.md`.

## Entrada mínima obrigatória

1. Leia `continuity/HANDOFF_CURRENT.md`.
2. Leia `continuity/STATUS.md`.
3. Leia `continuity/ACTIVE_ROUND.md`.
4. Resolva o HEAD atual de `master` antes de qualquer escrita.
5. Se o charter não estiver `READY`, não implemente; siga o handoff ou registre o bloqueio.
6. Carregue somente as rotas necessárias à unidade ativa.

## Roteamento sob demanda

| Necessidade | Leia |
|---|---|
| objetivo, limites e mapa do programa | `CONTEXT.md` |
| charter autorizado e grafo da rodada | `continuity/ACTIVE_ROUND.md` |
| plano de longo prazo | `continuity/EXECUTION_PLAN.md` |
| início, execução, bloqueio e commit | `continuity/ROUND_PROTOCOL.md` |
| revisão do trabalho executado | `continuity/REVIEW_PROTOCOL.md` |
| rationale e decisões vigentes | `continuity/DECISIONS.md` e ADRs indicados |
| papéis orquestrador/executor | `docs/architecture/ORCHESTRATOR_EXECUTOR_MODEL.md` |
| arquitetura MAESTRO | `docs/architecture/MAESTRO_WORK_ARCHITECTURE.md` |
| limites entre repositórios | `docs/architecture/CROSS_REPOSITORY_BOUNDARIES.md` |
| contrato de especificação de rodada | `docs/specifications/ROUND_CHARTER_CONTRACT.md` |
| paralelismo e subagentes | `docs/specifications/PARALLEL_EXECUTION_POLICY.md` |
| critérios do programa e MCP | `docs/specifications/PROGRAM_SPECIFICATION.md` e a especificação da unidade |
| divisão integral do trabalho | `docs/specifications/WORK_BREAKDOWN.md` |
| provas já produzidas | `evidence/EVIDENCE_INDEX.md` |

Não carregue todos os arquivos por padrão. Amplie o contexto quando dependência, risco, conflito ou decisão exigir.

## Contrato de execução completa

- Execute todas as tarefas, validações e entregas do charter, inclusive dependências inevitáveis.
- Não pare para relatório de progresso, tarefa longa, teste falhando, pesquisa necessária ou primeira abordagem malsucedida.
- Ao encontrar bloqueio em uma frente, continue todas as frentes independentes do DAG.
- Só pare por conclusão integral, bloqueio humano válido ou impossibilidade ambiental real após persistir estado seguro.
- Ao finalizar, marque o trabalho `EXECUTED_AWAITING_REVIEW`; somente o orquestrador pode registrar `ACCEPTED`.

## Paralelismo

Use subagentes quando as frentes forem independentes. Defina ownership de outputs e paths, evite edição concorrente de arquivos canônicos e mantenha integração, validação final e commit sob responsabilidade do executor principal.

## Invariantes operacionais

- Trabalhe exclusivamente em `master`; não crie branches, PRs ou worktrees secundárias.
- Cada rodada de IA termina com exatamente um commit atômico por repositório afetado, identificado por `Round-ID`.
- Trabalho cross-repo usa o mesmo `Round-ID` nos commits.
- Antes do commit, reconcilie o HEAD remoto; nunca use force push nem reescreva histórico.
- No mesmo commit da rodada, atualize implementação/documentação, `STATUS`, `HANDOFF_CURRENT`, `ACTIVE_ROUND`, `EVIDENCE_INDEX` e o registro em `continuity/rounds/`.
- Mudança incompleta só pode permanecer se segura, verificável e explicitamente marcada; caso contrário, reverta o trecho inseguro.
- Questões técnicas reversíveis são resolvidas dentro do mandato. Gates humanos seguem `ADR-0004` e `ADR-0005`.
- Não instale artefatos dinâmicos como `latest`; versões publicadas permanecem fixadas por URL e SHA256.
- Respeite caminhos obrigatórios de upgrade do GitLab e a matriz CE/EE, Debian e arquitetura.
- Nunca registre credenciais, tokens, segredos, backups ou dados pessoais.

## Bloqueio humano

Um bloqueio válido precisa indicar condição, evidência, tentativas, alternativas, decisão/recurso humano exato, tarefas já concluídas e estado seguro. O usuário e o orquestrador resolvem o gate; a retomada ocorre por charter revisado e novo `Round-ID` quando necessário.

## Fechamento obrigatório

A execução não termina até que todos os itens não bloqueados estejam concluídos, as validações proporcionais tenham sido executadas, as evidências estejam indexadas, o commit esteja em `master` e o pacote de revisão esteja pronto para o orquestrador.
