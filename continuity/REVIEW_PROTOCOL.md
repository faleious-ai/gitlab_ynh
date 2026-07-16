# Protocolo de revisão do orquestrador

## Entrada

O revisor recebe um charter em estado `EXECUTED_AWAITING_REVIEW`, os commits da rodada, round records, evidências, outputs de validação, riscos residuais e bloqueios.

## Revisão

O orquestrador:

1. reconcilia HEADs dos repositórios afetados;
2. compara entregas com cada tarefa e critério do charter;
3. verifica que alegações apontam para evidência;
4. inspeciona diff, testes, segurança, compatibilidade e continuidade;
5. confirma que subagentes foram integrados e que não há outputs órfãos;
6. distingue lacuna técnica de gate humano;
7. registra o resultado no repositório.

## Resultados

- `ACCEPTED`: critérios demonstrados; próximo charter pode ser preparado.
- `CORRECTION_REQUIRED`: há trabalho técnico executável; o orquestrador define rodada corretiva completa.
- `HUMAN_GATE`: falta decisão, credencial, autorização, custo ou escolha de consequência prática; usuário e orquestrador resolvem antes da retomada.
- `REJECTED_UNSAFE`: resultado não pode permanecer; exigir reversão ou compensação segura.

O Codex não marca o próprio trabalho como `ACCEPTED`; encerra em `EXECUTED_AWAITING_REVIEW` ou `BLOCKED_HUMAN`.

## Resolução de bloqueio

O orquestrador apresenta ao usuário somente a decisão necessária, alternativas, consequências e recomendação. Após a resposta, atualiza o charter ou cria revisão dele, explicita a decisão e libera nova rodada. O Codex então continua todo trabalho restante até conclusão ou próximo bloqueio válido.

## Persistência

Revisões que alterem estado, decisão ou plano geram round record e um único commit próprio em `master`. Comentários de issue podem resumir, mas não substituem a memória versionada.
