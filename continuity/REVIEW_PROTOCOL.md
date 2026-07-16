# Protocolo de revisão do orquestrador

## Fronteira remota

O orquestrador revisa somente estado persistido no GitHub. Arquivo, log ou evidência exclusivamente local não é revisável.

`EXECUTED_AWAITING_REVIEW` exige:

1. `baseline_head` e `round_head` completos;
2. todos os commits de tarefa publicados em `origin/master` dos repositórios afetados;
3. sequência `Task-ID → SHA → outputs → claims → evidências`;
4. commits e paths recuperáveis pelo GitHub;
5. mesmo `Round-ID` e `Charter-ID` na continuidade cross-repo;
6. pacote sem links locais e HEADs coincidentes.

Sem isso, o estado é `NOT_REVIEWABLE_REMOTE_SYNC_REQUIRED`, não um veredito técnico.

## Revisão por tarefa

Para cada commit, o orquestrador:

1. confirma Task-ID, escopo, dependências e atomicidade;
2. verifica ausência de trabalho não relacionado;
3. compara diff com claims, interfaces e invariantes;
4. exige seam público e evidência RED/GREEN para mudança comportamental;
5. inspeciona segurança, lifecycle, compatibilidade, simplicidade e reversibilidade;
6. confirma que claims não excedem o nível de prova;
7. avalia se o commit pode ser revertido seletivamente ou se suas dependências estão explícitas.

## Revisão integrada

Depois dos commits individuais, revisar `baseline_head...round_head` para detectar regressões de interação, interface drift, outputs órfãos, inconsistência cross-repo, documentação divergente e lacunas fora dos testes focais.

## Eixos independentes

- **Spec/Charter:** requisitos ausentes/parciais, scope creep, interface errada e claim sem prova.
- **Engineering:** bugs, segurança, lifecycle, compatibilidade, operabilidade, qualidade e reversibilidade.

Um eixo não mascara o outro.

## Estados de evidência

- `STRUCTURALLY_OBSERVED`: forma/presença inspecionada, sem execução.
- `LOCAL_VERIFIED`: comportamento executado localmente.
- `REMOTE_CI_VERIFIED`: run remoto do SHA confirmado.
- `LIFECYCLE_VERIFIED`: lifecycle proporcional executado.
- `UNVERIFIED` e `FAILED`.

Busca textual, ausência de erro ou fixture isolada não promovem claim comportamental.

## Resultados

- `ACCEPTED`: critérios materiais demonstrados e limitações classificadas corretamente.
- `CORRECTION_REQUIRED`: lacuna técnica executável; criar tarefas corretivas.
- `HUMAN_GATE`: decisão, acesso, custo, privilégio ou consequência prática depende do usuário.
- `REJECTED_UNSAFE`: exigir reversão seletiva de commit ou compensação segura.

O Codex não aceita o próprio trabalho.

## Persistência

A revisão é rodada de orquestração com tarefas próprias. Cada decisão ou mudança normativa recebe commit de tarefa publicado; não há squash. Comentário de issue não substitui memória versionada.
