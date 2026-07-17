# Work breakdown do programa v2

A lista executável está em `continuity/PROGRAM_BACKLOG.json`. Este documento é a visão humana e não duplica status mutável.

| WP | Objetivo | Owner principal | Gate material |
|---|---|---|---|
| WP-00 | governança e arquitetura executável | coordenador | nenhum |
| WP-01 | baseline dos instaladores | coordenador + Runner | nenhum |
| WP-02 | autoupdate e lifecycle Runner | Runner | promoção/registro real |
| WP-03 | autoupdate e lifecycle GitLab | coordenador | promoção/deploy |
| WP-04 | mirrors upstream | ambiente GitHub autorizado | criação de repositórios |
| WP-05 | repositório e núcleo MCP | futuro `gitlab-mcp` | criação/migração de repo |
| WP-06 | catálogo REST/GraphQL e paridade | MCP/coordenador | credencial de schema quando necessária |
| WP-07 | ondas funcionais MCP | MCP | mutações privilegiadas/destrutivas |
| WP-08 | assurance, coverage e sandbox | MCP + pacotes | ambiente controlado |
| WP-09 | release e manutenção | todos | release/deploy/produção |

O motor verifica que WP-00…WP-09 e objetivos T1…T8 permanecem cobertos.
