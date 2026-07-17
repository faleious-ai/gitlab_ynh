# Acceptance specification — GitLab MCP foundation

## Objetivo

Criar `faleious-ai/gitlab-mcp` como servidor MCP separado, testável e extensível, com lifecycle correto, descoberta de capabilities, ferramentas de leitura paginadas, erros estáveis, `trace_id` e bloqueio de operações destrutivas sem confirmação/autorização.

## Ownership

O Orquestrador controla este documento e `tests/acceptance/test_gitlab_mcp_foundation.py`. O Executor pode implementar o servidor e adicionar testes mais estritos, mas não reduzir o oracle. Divergência material usa `TEST_CONTRACT_CHALLENGE`.

## Repositório e seam

O teste procura o repositório em `GITLAB_MCP_ROOT` ou, por padrão, no sibling `../gitlab-mcp` e executa:

```text
python3 <gitlab-mcp>/server.py --stdio
```

O servidor processa mensagens JSON-RPC 2.0 delimitadas por newline e encerra de forma limpa após EOF. Em `GITLAB_MCP_TEST_MODE=1`, usa transporte GitLab fixture-only e não requer rede ou credencial.

## Protocolo

- negociar MCP `2025-11-25` no `initialize` quando solicitado e suportado;
- inicialização deve ser a primeira interação;
- `tools/list` expõe schemas estáveis;
- toda resposta tem JSON-RPC 2.0 e id correspondente;
- todo resultado contém `_meta.trace_id` ou equivalente definido pelo schema;
- todo erro contém código estável, mensagem curta e `data.trace_id`;
- stdout contém apenas protocolo; logs vão para stderr sem segredos.

## Catálogo mínimo

- `gitlab.capabilities`: descreve versão do servidor, edição/capabilities conhecidas e domínios planejados;
- `gitlab.projects.list`: leitura paginada com `items` e `next_page` explícitos;
- `gitlab.projects.delete`: pode ser anunciado para provar policy metadata, mas uma chamada sem autorização e confirmação deve falhar antes do transporte.

Ferramentas devem declarar classificação operacional: leitura, escrita reversível, privilegiada ou destrutiva. Ferramenta destrutiva exige confirmação válida e autorização correspondente; ausência produz `CONFIRMATION_REQUIRED` sem efeito.

## Segurança

- nenhum token em argv, stdout, stderr, fixture ou evidência;
- test mode não pode atingir rede;
- schemas rejeitam argumentos desconhecidos quando material;
- paginação possui limite máximo;
- ferramenta não implementada retorna erro estável, não traceback;
- nenhuma operação destrutiva ocorre no acceptance pack.

## Acceptance command

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.acceptance.test_gitlab_mcp_foundation -v
```

Baseline esperado: `RED`, porque o repositório/servidor ainda não existe.

Fontes normativas observadas em 2026-07-17:

- `https://modelcontextprotocol.io/docs/learn/versioning` — versão corrente `2025-11-25`;
- especificação MCP e JSON-RPC 2.0;
- API GitLab oficial para schemas e paginação nas ondas posteriores.
