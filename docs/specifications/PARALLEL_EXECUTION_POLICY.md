# Política de execução paralela e subagentes

## Princípio

Paralelizar por independência demonstrada, não por quantidade de agentes. O executor principal permanece responsável pelo resultado integrado.

## Decomposição

Antes de delegar, construir um DAG com:

- tarefa e output esperado;
- dependências de entrada;
- paths permitidos;
- arquivos compartilhados proibidos;
- validação local;
- critério de merge;
- risco e condição de escalonamento.

## Frentes adequadas

Podem rodar em paralelo quando não dependem do resultado umas das outras, por exemplo:

- auditorias de repositórios diferentes;
- levantamento de manifests, scripts, testes e workflows;
- pesquisa de upstream e documentação oficial;
- matrizes de API por domínios independentes;
- criação de fixtures e testes de módulos separados;
- revisão de segurança e revisão de lifecycle sobre outputs estáveis.

## Frentes sequenciais

Permanecem sequenciais quando envolvem:

- decisão arquitetural que redefine as demais tarefas;
- edição concorrente do mesmo arquivo canônico;
- migração, publicação, release ou operação destrutiva;
- integração que depende de contratos ainda não estabilizados;
- validação final e commit.

## Contrato do subagente

Cada subagente recebe contexto mínimo e retorna:

1. escopo executado;
2. fatos com paths, commits ou fontes;
3. alterações propostas ou produzidas;
4. testes/comandos e resultados;
5. desconhecidos, riscos e conflitos;
6. afirmação explícita de que não cometeu nem expandiu escopo.

## Integração

Somente o executor principal pode:

- alterar documentos canônicos compartilhados;
- resolver conflito entre subagentes;
- declarar critérios satisfeitos;
- executar validação integrada;
- atualizar continuidade;
- criar o commit da rodada.

## Falha parcial

Falha de uma frente não suspende frentes independentes. O executor continua todo trabalho não bloqueado, tenta estratégias alternativas e só registra bloqueio humano depois de esgotar caminhos técnicos razoáveis e concluir o restante do DAG.
