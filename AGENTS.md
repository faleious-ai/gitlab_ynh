# AGENTS.md

## Missão

Manter o pacote YunoHost do GitLab e coordenar o programa de autoupdate seguro, GitLab Runner, espelhos upstream e MCP GitLab. O repositório é a fonte de verdade; contexto de chat nunca é autoridade.

## Entrada mínima obrigatória

1. Leia `continuity/HANDOFF_CURRENT.md`.
2. Leia `continuity/STATUS.md`.
3. Resolva o HEAD atual de `master` antes de qualquer escrita.
4. Siga apenas as rotas abaixo necessárias à unidade ativa.

## Roteamento sob demanda

| Necessidade | Leia |
|---|---|
| objetivo, limites e mapa do programa | `CONTEXT.md` |
| próxima unidade executável | `continuity/EXECUTION_PLAN.md` |
| protocolo de início, execução e fechamento | `continuity/ROUND_PROTOCOL.md` |
| rationale e decisões vigentes | `continuity/DECISIONS.md` e ADRs indicados |
| arquitetura de trabalho MAESTRO | `docs/architecture/MAESTRO_WORK_ARCHITECTURE.md` |
| limites entre repositórios | `docs/architecture/CROSS_REPOSITORY_BOUNDARIES.md` |
| critérios do programa e MCP | `docs/specifications/PROGRAM_SPECIFICATION.md` e a especificação da unidade |
| divisão integral do trabalho | `docs/specifications/WORK_BREAKDOWN.md` |
| provas já produzidas | `evidence/EVIDENCE_INDEX.md` |

Não carregue todos os arquivos por padrão. Leia somente o contexto necessário e amplie quando uma dependência, risco ou decisão exigir.

## Invariantes operacionais

- Trabalhe exclusivamente em `master`; não crie branches, PRs ou worktrees secundárias.
- Cada rodada de IA termina com exatamente um commit atômico neste repositório, identificado por `Round-ID`.
- Antes do commit, reconcilie o HEAD remoto; nunca use force push nem reescreva histórico.
- No mesmo commit da rodada, atualize código/documentação afetados, `STATUS`, `HANDOFF_CURRENT`, `EVIDENCE_INDEX` e o registro em `continuity/rounds/`.
- Mudança incompleta só pode ser persistida se o estado continuar executável, verificável e claramente marcado; caso contrário, reverta o trecho inseguro e registre o bloqueio.
- O agente decide autonomamente questões técnicas reversíveis dentro das decisões vigentes. Escale somente gates humanos definidos em `ADR-0004`.
- Não instale artefatos dinâmicos como `latest`: versões publicadas permanecem fixadas por URL e SHA256.
- Respeite caminhos obrigatórios de upgrade do GitLab, matriz CE/EE, Debian e arquitetura.
- Nunca registre credenciais, tokens, segredos, backups ou dados pessoais.
- Pare apenas diante de bloqueio humano, ambiental ou de segurança real; registre causa, evidência e ação necessária.

## Fechamento obrigatório

Uma rodada não está encerrada até que validações proporcionais sejam executadas, evidências sejam indexadas, o próximo passo esteja explícito no handoff e o commit final esteja em `master`.