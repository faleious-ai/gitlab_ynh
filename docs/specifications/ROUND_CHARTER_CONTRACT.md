# Contrato de especificação de rodada

`continuity/ACTIVE_ROUND.md` é a autorização executável do Codex. Uma rodada só pode ficar `READY` quando o orquestrador tiver eliminado ambiguidades materiais e definido como o resultado será persistido e revisado remotamente.

## Estados

- `DRAFT`: perguntas ou decisões pendentes; Codex não executa.
- `READY`: autorizado para execução integral.
- `IN_PROGRESS`: execução iniciada.
- `LOCAL_COMPLETE_AWAITING_SYNC`: tarefas e validações concluídas, mas o commit existe apenas localmente.
- `REMOTE_SYNC_BLOCKED`: o resultado local está seguro, porém não foi publicado por falha de push, credencial, divergência ou indisponibilidade.
- `BLOCKED_HUMAN`: todo trabalho independente e toda persistência possível terminaram; resta gate humano explícito.
- `EXECUTED_AWAITING_REVIEW`: executor concluiu e publicou os commits em `origin/master`; ainda não aceito.
- `ACCEPTED`: revisor confirmou critérios e evidências remotas.
- `CORRECTION_REQUIRED`: revisão encontrou lacunas; nova rodada deve ser especificada.
- `SUPERSEDED`: substituído por charter posterior.

## Regra de transição

`IN_PROGRESS` não pode transitar diretamente para `EXECUTED_AWAITING_REVIEW` sem:

1. commit local final;
2. push fast-forward para `origin/master`;
3. confirmação de `HEAD == origin/master`;
4. SHA completo recuperável pelo GitHub;
5. evidências e continuidade acessíveis no remoto.

Commit apenas local transita para `LOCAL_COMPLETE_AWAITING_SYNC`. Falha de sincronização transita para `REMOTE_SYNC_BLOCKED`, não para aceite nem para bloqueio humano de produto.

## Campos obrigatórios

1. `Charter-ID` e estado;
2. objetivo observável;
3. perguntas feitas e decisões humanas recebidas, ou declaração de que nenhuma era necessária;
4. escopo e fora de escopo;
5. repositórios e paths autorizados;
6. entradas canônicas e `origin/master` baseline;
7. tarefas completas e dependências;
8. plano de paralelismo e ownership de outputs;
9. critérios de aceite e Definition of Done;
10. validações e evidências esperadas;
11. riscos, rollback e gates humanos;
12. condições válidas de bloqueio;
13. política de commit, push, reconciliação e handoff;
14. pacote remoto de revisão esperado, com SHAs completos e paths/URLs do GitHub.

## Perguntas pré-rodada

O orquestrador pergunta apenas o necessário para fechar decisões com consequência prática, incluindo quando aplicável:

- resultado e prioridade;
- comportamento e compatibilidade que devem ser preservados;
- versões, ambientes e plataformas alvo;
- custo, prazo ou consumo aceitável;
- acesso a credenciais ou infraestrutura;
- capacidade do executor de publicar em `origin/master`;
- operações destrutivas, publicação e exposição externa;
- trade-offs de produto, segurança, privacidade ou manutenção;
- critérios pelos quais o usuário considerará a rodada correta.

Questões puramente técnicas, reversíveis e cobertas pelo mandato são decididas pelo orquestrador e registradas com rationale.

## Definition of Done mínima

Todo charter deve declarar explicitamente que:

- commit local não basta;
- a rodada produz exatamente um commit final por repositório afetado;
- o commit é publicado em `origin/master` sem force push;
- os HEADs local e remoto coincidem;
- o pacote de revisão contém SHAs completos e evidências remotas;
- caminhos locais, como `C:/...`, não substituem arquivos versionados.

## Orientação anexada ao prompt

`Leia AGENTS.md e continue` executa o charter ativo. Uma orientação adicional pode esclarecer prioridade, restrição ou decisão humana. O executor deve registrá-la no round record. Ela não autoriza expansão silenciosa de missão, operação irreversível ou conflito com decisão canônica; nesses casos, registra bloqueio para o orquestrador.