# ADR-0001 — Branch única e commit por rodada

Status: `ACCEPTED`  
Data: 2026-07-16

## Contexto

O proprietário determinou desenvolvimento exclusivamente em `master`, sem branches secundárias, e persistência ao fim de cada rodada de IA. O fluxo precisa preservar continuidade sem depender de PRs.

## Decisão

- Toda escrita ocorre em `master`.
- É proibido criar branch ou worktree secundária para desenvolvimento normal.
- Cada rodada produz exatamente um commit atômico por repositório afetado.
- Trabalho cruzado usa o mesmo `Round-ID` em todos os commits.
- O agente reconcilia o HEAD antes de escrever e novamente antes do commit.
- Force push e reescrita de histórico são proibidos.
- Status, handoff, evidência e registro da rodada integram o mesmo commit da mudança.

## Consequências

Positivas:

- retomada simples;
- estado publicado imediatamente;
- proveniência ligada a uma unidade de execução;
- menor sobrecarga operacional.

Trade-offs:

- não há isolamento por branch;
- conflitos concorrentes precisam ser detectados antes do commit;
- commits devem ser coesos e o estado intermediário não pode quebrar `master`;
- revisão ocorre por diff, testes, evidência e histórico, não por PR.

## Controles compensatórios

- escopo pequeno e verificável;
- validação antes do commit;
- um único escritor por unidade quando possível;
- reconciliação de HEAD sem force;
- rollback por revert de commit completo;
- registros append-only de rodada.