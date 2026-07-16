# Lacunas de autoupdate — GitLab YunoHost

Round-ID: RND-20260716-003
Estado: baseline; nenhuma correção implementada

## Mecanismo atual

O workflow .github/workflows/updater.yml roda manualmente ou diariamente às
06:00 UTC. Ele faz checkout, executa .github/workflows/updater.sh, commita
quando PROCEED=true e chama peter-evans/create-pull-request para uma branch
ci-auto-update-v<VERSION> com base testing.

O updater.sh:

1. lê a versão com yq;
2. executa python upgrade-path.py 16.9.0;
3. lê a versão renderizada;
4. só compara versões com dpkg;
5. marca PROCEED=true sem executar linter, testes de matriz, package_check,
   instalação, upgrade, restore ou inspeção de diff.

upgrade-path.py consulta path.json, índices Packages.gz, renderiza
manifest.toml.j2 e baixa o template Omnibus de gitlab.rb. Ele grava diretamente
manifest.toml e conf/gitlab.rb, sem modo dry-run ou staging atômico.

## Lacunas observadas

| ID | Severidade | Evidência | Lacuna e consequência |
|---|---|---|---|
| GL-AU-01 | P0 | tests do workflow:16-27; ambiente auditado | yq e jinja2 não são instalados nem versionados pelo workflow. Em um runner limpo, o updater pode falhar antes de gerar qualquer diff. |
| GL-AU-02 | P0 | workflow:43-45; refs da fork | o workflow aponta PR para testing e cria branch, enquanto a fork só expõe master e a política exige master-only. A automação não corresponde ao contrato de governança. |
| GL-AU-03 | P1 | updater.sh:21-62 | não há validação do diff gerado, dos matches de patch em gitlab.rb, da matriz completa, do package linter ou de lifecycle antes de PROCEED=true. |
| GL-AU-04 | P1 | upgrade-path.py:289-359 | re.sub aplica patches sem afirmar que cada padrão foi encontrado; mudança silenciosa do template upstream pode produzir configuração incompleta. |
| GL-AU-05 | P1 | upgrade-path.py:97-190 | a resolução exige todos os CE/EE × arquitetura de cada distribuição, mas não persiste relatório de células ausentes, fonte consultada, versão do índice ou motivo de exclusão. |
| GL-AU-06 | P1 | upgrade-path.py:268-270 e 357-359 | manifest e gitlab.rb são escritos diretamente; não há geração em diretório temporário, validação e substituição atômica do conjunto. |
| GL-AU-07 | P1 | upgrade-path.py:193-230; scripts/upgrade:106-157 | o caminho gerado e o caminho consumido são implementações separadas, baseadas em parsing textual do manifest, sem teste diferencial contra path.json. |
| GL-AU-08 | P1 | workflow:16-49 | ação, dependências e create-pull-request usam tags de ação e não há pin por SHA nem registro de provenance dos binários/fontes consultados. |
| GL-AU-09 | P2 | .gitlab-ci.yml:1-7 | CI executa somente package_linter em Python 3.5 e clona o linter sem pin. Não cobre o gerador nem lifecycle. No ambiente atual o linter não pôde rodar por falta de jsonschema. |
| GL-AU-10 | P2 | tests.toml | há cenários de package_check, mas nenhum teste unitário do gerador, da matriz de assets, de idempotência ou de falha fechada. |
| GL-AU-11 | P2 | snapshot de rede em 2026-07-16 | path.json retornou alvo 19.1.2 e os índices tinham as 12 células CE/EE × Debian × arquitetura; o manifest permaneceu em 19.1.0~ynh1. A atualização está pendente, não aplicada. |

## Backlog ordenado

| Ordem | Unidade | Dependências | Critério observável |
|---:|---|---|---|
| 1 | GL-AU-01/02: normalizar executor master-only e instalar dependências reprodutíveis | ADR de governança já aceito | workflow executa em runner limpo, escreve somente em master conforme política e deixa artefato de diagnóstico |
| 2 | WP-03A: fonte de release GitLab e fixture congelada | WP-01 | fixture documenta path.json, versão, edição, Debian, arquitetura, URL e SHA256 sem depender de rede em teste |
| 3 | WP-03B: resolver upgrade path | WP-03A | casos de origem/destino, parada obrigatória, versão ausente, duplicata e salto indevido são testados |
| 4 | WP-03C/03D: resolver matriz e gerar manifest | WP-03A/03B | todas as células obrigatórias são resolvidas, ausência aborta sem escrita, saída é determinística e idempotente |
| 5 | GL-AU-04/06: patch de gitlab.rb com contrato | WP-03D | cada transformação exige match, placeholders restantes falham, arquivo final passa validação e o conjunto é publicado atomicamente |
| 6 | WP-03E: lifecycle e assurance | WP-03D | package_linter, install, upgrade, backup/restore, Pages, CE/EE e health têm evidência indexada em ambiente controlado |
| 7 | GL-AU-11: promover 19.1.2 somente após os gates | 1-6 e revisão do orquestrador | commit único contém manifest, template/config, evidência, testes e decisão de aceite; sem download runtime de latest |

## Decisões que permanecem fora desta rodada

Não foram alterados versão, URL, hash, workflow, branches, regras ou
comportamento de instalação. A automação futura deve manter assets fixados e
não transformar latest em resolução em tempo de instalação.
