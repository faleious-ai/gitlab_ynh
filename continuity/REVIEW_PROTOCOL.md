# Protocolo de revisão v2

O Orquestrador revisa somente material remoto. Para cada task receipt:

1. resolve o commit que adicionou o receipt;
2. confirma Task-ID no subject e ancestralidade em `origin/master`;
3. confere ownership de paths, evidências no commit e gates pass;
4. revisa Spec/Charter e Engineering/Security/Lifecycle;
5. registra override `accepted`, `correction_required`, `blocked_human` ou `superseded` em tarefa de orquestração.

A revisão integrada verifica backlog coverage, findings, queue freshness, CI/lifecycle e ausência de trabalho fora da fila. `eligible_tasks=[]` isolado nunca é aceite.
