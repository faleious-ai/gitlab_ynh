# Divergência contra upstream — GitLab YunoHost

Round-ID: RND-20260716-003
Snapshot da fork: master em e2d79f37aeeb765c53c9474f1ea6da3b8ac238b8
Snapshot YunoHost-Apps: master em b0a6918705efd0c018e7ede7a77cb57021da8f0c

## Método

Foram clonados os dois repositórios públicos e comparados os históricos,
árvores e arquivos funcionais. O merge-base é exatamente o HEAD atual de
YunoHost-Apps/gitlab_ynh. A fork contém 27 caminhos adicionais, todos de
continuidade, arquitetura, decisões, especificações, evidências e protocolos.
Não há divergência funcional no snapshot:

- manifest.toml, manifest.toml.j2 e upgrade-path.py são iguais;
- scripts de install, upgrade, backup, restore, change_url, config, remove e
  _common.sh são iguais;
- conf, config_panel, tests, .gitlab-ci.yml e workflow updater são iguais.

## Classificação

| Classe | Fatos |
|---|---|
| Herdada | Todo comportamento de empacotamento e o workflow de atualização vêm do upstream YunoHost-Apps. |
| Local deliberada | AGENTS.md, CONTEXT.md, continuity/, docs/architecture, docs/decisions, docs/specifications, docs/planning e evidence/. |
| Atualização pendente | O snapshot declara 19.1.0~ynh1; o path.json oficial consultado em 2026-07-16 indicava 19.1.2 e os 12 combinações CE/EE × 3 Debian × 2 arquiteturas estavam presentes nos índices de pacotes. Nenhuma atualização foi aplicada nesta rodada. |
| Incompatibilidade de governança | A fork declara master-only e um commit por rodada, mas o workflow herdado cria branch ci-auto-update-v<VERSION>, abre PR e usa base testing. O remoto da fork auditada possui apenas master. |
| Documentação upstream | README e badges continuam gerados no estilo YunoHost-Apps e refletem o baseline de 19.1.0; não foram modificados pela fork. |

## Upstream de produto e fontes

O manifest aponta o código do produto para
gitlab-org/gitlab, mas os binários são baixados de packages.gitlab.com. O
gerador usa ainda:

- path.json oficial para o caminho obrigatório de upgrade;
- template gitlab.rb do repositório gitlab-org/omnibus-gitlab;
- índices APT do pacote CE/EE para resolver SHA256.

Essas fontes são dependências externas do processo de atualização, não partes
versionadas da fork. A inspeção confirmou acesso HTTP ao path.json e ao
template Omnibus para 19.1.0; não foi feita uma comparação integral do enorme
repositório gitlab-org/gitlab.

## Estado de branches e proveniência

O remoto da fork auditada expõe apenas master e não possui tags publicadas no
snapshot. O upstream YunoHost-Apps também foi comparado em master. Portanto,
não existe uma branch testing local para receber o workflow herdado, nem uma
tag local que funcione como release reproduzível da fork.

## Conclusão

A fork é, no momento, um coordenador documental sobre um pacote upstream,
não uma implementação funcionalmente divergente. Qualquer atualização de
versão ou alteração de comportamento deve primeiro resolver a incompatibilidade
entre o workflow herdado e a política master-only, registrar a proveniência
das fontes e demonstrar o lifecycle em ambiente YunoHost.
