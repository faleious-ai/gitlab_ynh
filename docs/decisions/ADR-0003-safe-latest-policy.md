# ADR-0003 — Política de “latest” seguro

Status: `ACCEPTED`  
Data: 2026-07-16

## Contexto

O objetivo é manter os pacotes próximos da versão mais recente sem tornar instalações não reproduzíveis nem ignorar mandatory upgrade stops do GitLab.

## Decisão

“Latest” significa a versão estável mais recente que seja elegível para o estado atual e para a matriz suportada.

O processo automático deve:

1. consultar fonte de verdade autenticável;
2. filtrar pre-releases e versões incompatíveis;
3. resolver caminho de upgrade e etapas intermediárias;
4. localizar todos os assets por edição, Debian e arquitetura;
5. baixar ou consultar assets para calcular/verificar SHA256;
6. atualizar manifest e fixtures com versão, URL e hash fixos;
7. executar validações;
8. produzir commit revisável e auditável.

O instalador nunca deve resolver `latest` em runtime.

## Consequências

- uma versão nova pode ser deliberadamente adiada por caminho de upgrade, asset ausente ou falha de teste;
- CE e EE podem exigir matrizes distintas;
- atualização automática prepara mudança; não elimina validação;
- falha fechada é preferível a artefato não verificado.