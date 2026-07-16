# Arquitetura MAESTRO de trabalho

## Objetivo

Transformar o repositório em uma superfície de trabalho legível para humanos e agentes, na qual intenção, execução, validação, decisão e memória não dependam de uma sessão específica.

## Princípio central

O modelo descreve, propõe e executa; a arquitetura de trabalho limita, verifica e persiste; o humano mantém autoridade sobre missão, risco e irreversibilidade.

A velocidade de geração não conta como conclusão. Uma mudança só é promovida quando é compreensível, delimitada, verificável, auditável, reversível e continuável.

## Camadas MAESTRO aplicadas

### 1. Intenção

Origem: usuário, issue ou incidente.

Artefato: objetivo explícito e consequência desejada.

Controle: nenhuma execução começa a partir de intenção ambígua que possa alterar missão ou risco.

### 2. Especificação

Origem: `docs/specifications/`, issue ativa e critérios de aceite.

Artefato: escopo, fora de escopo, invariantes, entradas, saídas, falhas e Definition of Done.

Controle: o agente não preenche silenciosamente lacunas de produto; registra pressupostos técnicos reversíveis.

### 3. Contexto

Origem: `AGENTS.md` roteia; `CONTEXT.md` fornece mapa estável; arquivos adicionais são lidos sob demanda.

Controle: contexto mínimo suficiente. Carregar tudo é tratado como risco de ruído; carregar pouco demais é tratado como risco de cegueira.

### 4. Contratos e fronteiras

Origem: manifest, scripts, testes, especificações, ADRs e limites entre repositórios.

Controle: superfície de mudança declarada, invariantes preservados, operações privilegiadas separadas.

### 5. Execução

Origem: work package ativo.

Controle: unidade coerente, ciclos de tentativa-erro-aprendizado, sem branches secundárias e sem alterar áreas fora do mandato.

### 6. Validação

Origem: testes, lint, verificações de integridade, contract tests, inspeção de diff e evidência reproduzível.

Controle: prova proporcional ao risco. Alegação não demonstrada permanece `UNVERIFIED`.

### 7. Governança e decisão

Origem: `continuity/DECISIONS.md`, ADRs e gates de `ADR-0004`.

Controle: autonomia técnica ampla; escalonamento humano apenas por missão, risco material, segredo, irreversibilidade, custo ou publicação.

### 8. Memória e continuidade

Origem: status, handoff, plano, round records, evidence index e Git.

Controle: todo ciclo termina com estado persistido no mesmo commit da mudança.

## Máquina de estados da rodada

```text
READY
  -> SCOPED
  -> EXECUTING
  -> VALIDATING
  -> PERSISTING
  -> COMMITTED
  -> READY
```

Estados de exceção:

```text
EXECUTING|VALIDATING -> BLOCKED
EXECUTING|VALIDATING -> REVERTING -> PERSISTING
```

Regras:

- `SCOPED` exige critérios de aceite e superfície de mudança.
- `VALIDATING` exige execução real dos checks aplicáveis.
- `PERSISTING` exige atualização das memórias canônicas.
- `COMMITTED` exige um commit atômico em `master`.
- `BLOCKED` exige evidência e pedido humano concreto.

## Papéis

### Maestro Diretor humano

Define missão, valores, tolerância a risco, consequências práticas aceitáveis e gates Classe C. Não precisa decidir detalhes técnicos delegados.

### Agente executor

Recupera contexto, escolhe abordagem técnica, implementa, testa, registra rationale e fecha a rodada. Não aprova por conta própria uma operação Classe C.

### Agente verificador

Pode ser outro modelo, teste, pipeline ou a mesma IA em fase separada. Procura contradições, regressões, claims sem evidência e violações de fronteira.

### Repositório/máquina

Conserva contratos, histórico, testes e estado. É a memória operacional autoritativa.

## Memória em camadas

| Camada | Arquivo | Volatilidade |
|---|---|---|
| orientação | `AGENTS.md` | baixa |
| contexto | `CONTEXT.md` | baixa |
| contrato | `docs/specifications/` | média |
| rationale | `docs/decisions/` | baixa |
| estado | `continuity/STATUS.md` | alta |
| retomada | `continuity/HANDOFF_CURRENT.md` | alta |
| sequência | `continuity/EXECUTION_PLAN.md` | média |
| prova | `evidence/EVIDENCE_INDEX.md` | append/update |
| proveniência | `continuity/rounds/` e Git | append-only |

## Política de promoção

- descoberta de rodada -> registro de rodada;
- fato que altera estado -> `STATUS`;
- próximo passo -> `HANDOFF`;
- decisão durável -> ADR + índice;
- contrato novo -> especificação;
- prova -> evidence index;
- princípio estável -> contexto ou AGENTS.

Não duplicar o mesmo conteúdo em múltiplas autoridades. Referenciar a fonte canônica.

## Reversibilidade

Cada commit de rodada deve poder ser revertido como unidade lógica. Mudanças de dados, permissões, credenciais ou produção requerem plano de rollback demonstrado antes da ação.

## Critério de maturidade desta arquitetura

A arquitetura funciona quando um agente sem memória da conversa consegue:

1. identificar o estado atual em menos de três leituras obrigatórias;
2. localizar contexto adicional por rota explícita;
3. saber o que pode decidir sozinho;
4. executar a próxima unidade sem reconstruir rationale;
5. demonstrar o resultado;
6. deixar um commit e handoff coerentes para o agente seguinte.