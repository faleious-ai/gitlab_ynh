# Especificação de autoupdate do pacote GitLab

Status: `PLANNED`  
Work package: `WP-03`

## Objetivo

Gerar mudanças reproduzíveis para uma versão estável elegível do GitLab CE/EE, cobrindo distribuições Debian e arquiteturas suportadas, sem saltar mandatory upgrade stops.

## Entradas

- versão atual do pacote YunoHost;
- edição instalada ou matriz CE/EE;
- distribuição Debian suportada;
- arquitetura;
- fonte oficial de releases/pacotes;
- política oficial de upgrade paths;
- manifest e fixtures atuais.

## Saídas

- versão YunoHost proposta;
- matriz de URLs por edição/distribuição/arquitetura;
- SHA256 verificado para cada asset;
- caminho de upgrade completo, incluindo stops intermediários;
- diff determinístico de manifest/fixtures;
- relatório de validação e falhas;
- registro de proveniência da fonte.

## Algoritmo normativo

1. detectar versão atual e matriz declarada;
2. consultar fonte oficial e selecionar release estável, excluindo pre-release;
3. calcular elegibilidade do destino;
4. consultar regras de upgrade e construir grafo origem -> stops -> destino;
5. rejeitar destino se o caminho não for demonstrável;
6. resolver assets CE/EE por Debian e arquitetura;
7. rejeitar atualização se qualquer célula obrigatória estiver ausente;
8. obter e verificar tamanho, URL final e SHA256;
9. gerar alterações em ordem estável;
10. validar consistência da versão em todos os arquivos;
11. executar testes unitários/fixtures e subset aplicável de lifecycle;
12. produzir commit de rodada e evidência.

## Invariantes

- instalação nunca consulta `latest`;
- todas as URLs publicadas são imutáveis ou versionadas;
- todos os downloads possuem SHA256;
- CE e EE não podem compartilhar hash presumido;
- nenhuma arquitetura declarada pode ficar sem asset;
- versão do manifest e nomes dos sources permanecem coerentes;
- upgrade direto inválido deve falhar antes de modificar o sistema;
- falhas de rede ou fonte não geram manifest parcial.

## Política de upgrade

O resolver deve representar versões como nós e stops obrigatórios como restrições. Deve retornar:

- `DIRECT_ALLOWED`;
- `INTERMEDIATE_STOPS_REQUIRED` com sequência ordenada;
- `UNSUPPORTED_OR_UNKNOWN` com rationale e fonte ausente.

Não assumir que a versão numericamente mais recente é diretamente instalável sobre qualquer origem.

## Casos de teste mínimos

- versão nova válida para toda a matriz;
- release pre-release ignorada;
- asset ausente em uma arquitetura;
- hash divergente;
- CE disponível e EE ausente, e vice-versa;
- caminho direto válido;
- um e múltiplos stops obrigatórios;
- origem antiga sem caminho conhecido;
- repetição idempotente sem diff;
- ordem determinística de output;
- falha de rede sem escrita parcial;
- atualização de package version YunoHost coerente.

## Validação de pacote

Conforme impacto:

- lint/schema do manifest;
- testes de sources;
- clean install;
- upgrade por cada stop relevante;
- backup/restore;
- change URL;
- configuração CE/EE;
- remoção;
- arquiteturas suportadas ou validação equivalente disponível.

## Evidência necessária

- fonte e timestamp da release;
- caminho de upgrade calculado;
- lista de assets e hashes;
- comandos/testes e resultados;
- diff final;
- riscos residuais.

## Falha segura

O updater deve sair sem alterar arquivos quando qualquer requisito obrigatório não puder ser verificado. Saída parcial é considerada defeito.