# Protocolo de revisão do orquestrador

## Fronteira de revisão

O orquestrador revisa somente estado persistido no GitHub. Commit, arquivo, log ou evidência existente apenas no computador do executor não é acessível nem revisável.

`EXECUTED_AWAITING_REVIEW` é válido somente quando:

1. os SHAs completos da rodada estão publicados em `origin/master` de todos os repositórios afetados;
2. os commits podem ser obtidos pelo GitHub;
3. os paths citados existem no remoto;
4. o pacote usa URLs/paths remotos, não links locais;
5. a continuidade remota registra o mesmo `Round-ID` e `Charter-ID`.

Se essas condições falharem, o trabalho não recebe veredito técnico. O estado é `NOT_REVIEWABLE_REMOTE_SYNC_REQUIRED`, derivado de `LOCAL_COMPLETE_AWAITING_SYNC` ou `REMOTE_SYNC_BLOCKED`.

## Entrada

O revisor recebe um charter em estado remoto `EXECUTED_AWAITING_REVIEW`, os SHAs completos publicados, round records, evidências, outputs de validação, riscos residuais e bloqueios.

Links `C:/...`, paths de workspace, SHAs curtos não resolvíveis e alegações de push sem confirmação de `origin/master` não constituem entrada suficiente.

## Revisão

O orquestrador:

1. reconcilia os HEADs remotos dos repositórios afetados;
2. confirma que cada SHA informado é o HEAD esperado ou ancestral explicitamente autorizado;
3. compara entregas com cada tarefa e critério do charter;
4. verifica que alegações apontam para evidência remota;
5. inspeciona diff, testes, segurança, compatibilidade e continuidade;
6. confirma que subagentes foram integrados e que não há outputs órfãos;
7. distingue lacuna técnica de gate humano e de falha de sincronização;
8. registra o resultado no repositório.

## Resultados

- `ACCEPTED`: critérios demonstrados; próximo charter pode ser preparado.
- `CORRECTION_REQUIRED`: há trabalho técnico executável; o orquestrador define rodada corretiva completa.
- `HUMAN_GATE`: falta decisão, credencial, autorização, custo ou escolha de consequência prática; usuário e orquestrador resolvem antes da retomada.
- `REJECTED_UNSAFE`: resultado remoto não pode permanecer; exigir reversão ou compensação segura.

`NOT_REVIEWABLE_REMOTE_SYNC_REQUIRED` não é veredito sobre a qualidade do trabalho. Indica que o executor ainda não completou a persistência remota necessária para a revisão.

O Codex não marca o próprio trabalho como `ACCEPTED`; encerra em `EXECUTED_AWAITING_REVIEW`, `BLOCKED_HUMAN`, `LOCAL_COMPLETE_AWAITING_SYNC` ou `REMOTE_SYNC_BLOCKED` conforme o estado real.

## Resolução de sincronização

Quando o trabalho estiver apenas local, o orquestrador não reconstrói nem adivinha o diff. O executor deve:

1. buscar `origin/master`;
2. reconciliar o commit ainda não publicado sem force push;
3. repetir validações impactadas;
4. publicar em `origin/master`;
5. confirmar SHAs completos e arquivos remotos;
6. então alterar o estado para `EXECUTED_AWAITING_REVIEW`.

## Resolução de bloqueio humano

O orquestrador apresenta ao usuário somente a decisão necessária, alternativas, consequências e recomendação. Após a resposta, atualiza o charter ou cria revisão dele, explicita a decisão e libera nova rodada. O Codex então continua todo trabalho restante até conclusão ou próximo bloqueio válido.

## Persistência

Revisões que alterem estado, decisão ou plano geram round record e um único commit próprio publicado em `origin/master`. Comentários de issue podem resumir, mas não substituem a memória versionada.