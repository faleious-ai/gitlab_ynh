# ADR-0004 — Autonomia técnica e gates humanos proporcionais

Status: `ACCEPTED`  
Data: 2026-07-16

## Contexto

O usuário delega decisões técnicas para maximizar continuidade e volume de execução. Intervenção humana deve ocorrer apenas quando a decisão ultrapassa o mandato técnico ou produz consequência prática relevante e difícil de reverter.

## Decisão

### Classe A — Autonomia do agente

O agente decide, executa e registra sem solicitar aprovação para:

- escolhas técnicas reversíveis;
- organização interna de código e testes dentro dos contratos;
- ferramentas, formatos e algoritmos que não alterem missão ou risco;
- correções de lint, teste, documentação e refactors comprovadamente equivalentes;
- tentativas alternativas após falha, com aprendizado registrado.

### Classe B — Autonomia com registro reforçado

O agente pode decidir, mas deve criar ADR/evidência quando houver:

- mudança de contrato interno relevante;
- nova dependência;
- alteração de estratégia de atualização;
- mudança de permissões não privilegiadas;
- alteração de compatibilidade suportada;
- novo mecanismo de persistência ou observabilidade.

### Classe C — Gate humano obrigatório

Interromper antes da ação quando envolver:

- missão, escopo de produto ou filosofia de governança;
- licença, visibilidade, transferência, fork network ou publicação externa;
- custo financeiro ou compromisso operacional novo;
- acesso a segredo não provisionado;
- destruição, perda de dados, rotação/revogação de credenciais ou irreversibilidade relevante;
- ampliação material de privilégios ou superfície de exposição;
- escolha entre alternativas com consequências práticas mutuamente exclusivas para o usuário;
- release pública ou mudança que afete instância de produção sem rollback demonstrado.

## Consequências

O agente não deve pedir aprovação por detalhes técnicos comuns. Ao escalar, deve apresentar decisão concreta, alternativas, evidência, riscos e consequência prática, não uma pergunta vaga.