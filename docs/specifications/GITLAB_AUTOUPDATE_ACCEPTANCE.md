# Acceptance specification — GitLab autoupdate

## Objetivo

Gerar, sem promover automaticamente, um candidato completo e reproduzível para atualização do pacote YunoHost do GitLab. O candidato deve respeitar edition, Debian, arquitetura, checksums, origem oficial e required upgrade stops.

## Ownership

O Orquestrador controla este documento e `tests/acceptance/test_gitlab_autoupdate_objective.py`. O Executor não pode reduzir os casos ou alterar resultados esperados para obter GREEN; divergência real usa `TEST_CONTRACT_CHALLENGE`.

## Seam público esperado

```text
python3 scripts/gitlab_autoupdate.py resolve --catalog <json> --current <version> --target <version> --edition <ce|ee> --distribution <name> --architecture <arch>
python3 scripts/gitlab_autoupdate.py generate --catalog <json> --manifest <toml> --target <version> --output <candidate.toml>
```

A saída normal é JSON. Falhas de contrato usam código diferente de zero e JSON explicativo.

## Invariantes

- versões, URLs e SHA256 ficam explicitamente fixados;
- nunca resolver `latest` no install ou upgrade;
- fonte inicial pertence aos projetos oficiais `gitlab/gitlab-ce` ou `gitlab/gitlab-ee` em `packages.gitlab.com`;
- matriz mínima: CE/EE × bullseye/bookworm/trixie × amd64/arm64;
- cada URL identifica edition, distribuição, versão e arquitetura exatas;
- cada SHA256 tem 64 caracteres hexadecimais;
- required stops usam a última patch disponível de cada minor obrigatório;
- para GitLab 18: stops `18.2`, `18.5`, `18.8`, `18.11` quando atravessados;
- para GitLab 19: stops `19.2`, `19.5`, `19.8`, `19.11` quando atravessados;
- candidate generation é atômica, não modifica o manifest de entrada e não promove;
- pacote ausente, checksum ausente, edition divergente, distro/arch incompleta ou salto obrigatório ausente falham fechado;
- observação live e atualização de catálogo produzem artefatos novos com data e fonte; fixtures não provam freshness.

## Upgrade path

O resolver recebe versão atual e target e retorna todos os required stops estritamente entre ambas, usando a maior patch elegível de cada minor, seguida do target. O target pode coincidir com um required stop.

Nenhuma operação de upgrade real é autorizada por este acceptance pack. Background migrations, backup, health check e lifecycle real pertencem a gates posteriores.

## Acceptance command

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.acceptance.test_gitlab_autoupdate_objective -v
```

Baseline esperado: `RED`, porque `scripts/gitlab_autoupdate.py` ainda não existe.

Fontes normativas observadas em 2026-07-17:

- `https://docs.gitlab.com/update/upgrade_paths/`;
- `https://docs.gitlab.com/update/versions/gitlab_18_changes/`;
- `https://docs.gitlab.com/update/versions/gitlab_19_changes/`.
