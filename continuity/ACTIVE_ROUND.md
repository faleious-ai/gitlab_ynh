# Rodada ativa

Charter-ID: `CHR-WP02-002`  
Estado: `READY`  
Preparado em: 2026-07-16  
Orquestrador: ChatGPT com o Maestro Diretor  
Executor principal: Codex  
Unidade: `WP-02 Correção — confiança do updater Runner`

## Autorização

`Leia AGENTS.md e continue` autoriza a execução integral deste charter. O repositório funcional primário é `faleious-ai/gitlab-runner_ynh`. Este coordenador recebe síntese, decisões, evidências e continuidade com o mesmo novo `Round-ID`.

## Revisão anterior

`CHR-WP02-001` recebeu `CORRECTION_REQUIRED`. Registro local: `continuity/reviews/REV-RND-20260716-005.md`. Revisão detalhada no Runner: arquivo de mesmo path.

## Objetivo

Completar a cadeia de confiança e as capacidades faltantes da fundação Runner sem promover versão: descoberta oficial atual, checksums verificáveis, fronteira exata de origem, cópia candidata do manifest/diff guard, credencial fora de argv, contrato atual da action YunoHost e CI remoto verificável.

## Repositório primário e escopo

No Runner, executar integralmente `CHR-WP02-002` local, incluindo:

- API/freshness e allowlists;
- checksum oficial/assinatura ou recálculo equivalente;
- manifest candidato e diff limitado;
- transporte seguro da credencial e teste de argv;
- decisão demonstrada sobre action YunoHost;
- testes negativos e CI com referências imutáveis;
- relatórios de confiança e candidata sem promoção.

Neste coordenador:

- registrar síntese cross-repo, riscos, fontes e níveis de evidência;
- atualizar `STATUS`, `HANDOFF_CURRENT`, `ACTIVE_ROUND`, `EVIDENCE_INDEX` e round record;
- preservar decisões gerais do programa;
- usar o mesmo `Round-ID` do Runner.

## DAG paralelo no Runner

1. API/freshness/allowlists;
2. checksums/assinatura/fixtures;
3. manifest candidato/diff guard;
4. registro/action YunoHost;
5. testes/CI.

Subagentes não fazem commit. O executor principal integra arquivos canônicos, repete checks e publica.

## Fora de escopo

Promover versão, registrar ou remover Runner real, usar a credencial histórica, executar ação destrutiva em produção, publicar release, criar branch/PR/worktree, force push, reescrever histórico ou alterar ruleset/licença/visibilidade.

## Gate

`HG-RUN-SEC-01` permanece `UNRESOLVED_NO_AUTHORITY` e não bloqueia nenhuma tarefa. Nenhuma pergunta humana adicional é necessária.

## Definition of Done cross-repo

- todos os critérios do charter Runner `CHR-WP02-002` atendidos;
- manifest Runner rastreado ainda em `18.6.2~ynh1`;
- evidências distinguem descoberta online, fixture offline, checksum/signature e conteúdo;
- exatamente um commit publicado em `origin/master` por repositório afetado, mesmo `Round-ID`;
- `HEAD == origin/master`, árvores limpas e material recuperável pelo GitHub;
- estado `EXECUTED_AWAITING_REVIEW` nos dois repositórios.

## Pacote de revisão

SHAs completos, URLs remotas, matriz tarefa-output-evidência, fontes oficiais, relatórios, testes, CI, decisão da action, prova de credencial fora de argv, limitações e gate. Não declarar `ACCEPTED`.
