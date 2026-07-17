# Política de paralelismo e subagentes

## Regra

Paralelizar somente frentes com dependências, paths e outputs separáveis. O Codex permanece responsável pelo resultado integrado, pelos commits de tarefa e pela sincronização remota.

## DAG mínimo

Cada tarefa/frente declara Task-ID, dependências, entradas, claims, seam, outputs, paths autorizados, arquivos compartilhados proibidos, validação e commit que absorverá o resultado.

## Frentes adequadas

- auditoria upstream e packaging;
- manifest/sources e matriz de assets;
- lifecycle e service/config;
- tokens, redaction e segurança;
- testes/workflows;
- API/MCP e documentação oficial;
- síntese cross-repo, quando os inputs já estiverem estáveis.

## Frentes sequenciais

- decisões que redefinem contrato;
- edição de documentos canônicos compartilhados;
- integração cross-repo;
- revisão adversarial final;
- continuidade e evidências;
- criação/publicação de commits;
- operações reais, destrutivas ou irreversíveis.

## Ownership

Subagentes não criam commit, branch, PR, worktree ou push. Não editam simultaneamente o mesmo path. O executor integra uma tarefa por vez e executa seus gates antes do commit.

## Retorno do subagente

Task-ID, escopo, fatos/fontes, alterações, comandos/resultados, unknowns, riscos, dead ends e confirmação de ausência de commit/expansão.

## Integração

1. conferir ownership e dependências;
2. integrar outputs da tarefa;
3. executar TDD/gates no seam real;
4. revisar Spec/Charter e Engineering;
5. criar um commit da tarefa;
6. publicar e verificar antes da próxima escrita.

## Planejamento canônico

Depois do motor de execução ficar GREEN, `scripts/maestro_program.py plan` é a fonte executável para `eligible_tasks`, `blocked_tasks`, lanes e `integration_order`. A preparação de lanes pode sobrepor intervalos em paths separados, mas cada tarefa continua com commit e push próprios, em ordem serial.

## Falha parcial

Uma frente falha não suspende as demais. O Codex tenta alternativas, executa backprop, conclui trabalho independente e só então registra bloqueio. Falha de sincronização impede novos commits no mesmo repositório, mas não pesquisa ou trabalho independente sem escrita.
