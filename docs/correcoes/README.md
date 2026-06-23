# Correções do Static Checker — BobEnzo2026-1

Esta pasta documenta as correções aplicadas ao Static Checker para alinhá-lo à
**especificação oficial** (`Projeto2026-1 vSN1.0.pdf`), à **arquitetura**
(`EQ01PROJ`) e aos **autômatos** (`EQ01BRUT_OTIM`).

## Contexto
Uma validação completa (especificação → arquitetura → autômatos → código)
identificou que a engenharia estava sólida, mas a **saída do analisador léxico
não era aderente à especificação**: códigos de átomo inventados, sensibilidade a
maiúsculas invertida, uma palavra reservada faltando, uso indevido do código de
EOF e relatórios incompletos. O projeto estava **reprovável** na Etapa 7 (LEX).

## Documentos
- [`01-correcoes-aplicadas.md`](01-correcoes-aplicadas.md) — cada correção: o **quê**, o **porquê**, arquivos e antes/depois.
- [`02-decisoes-e-pendencias.md`](02-decisoes-e-pendencias.md) — decisões de projeto, simplificações conscientes e itens pendentes.
- [`03-pipeline-qualidade.md`](03-pipeline-qualidade.md) — resultado da pipeline de qualidade (.claude) e ações tomadas.

## Como verificar
```bash
# testes (37 casos)
python -m pytest -q

# execução de ponta a ponta
cp tests/fixtures/exemplo.261 ./exemplo.261
python run.py exemplo
cat exemplo.LEX exemplo.TAB
```

Resultado esperado: códigos conforme o Apêndice A (ex.: `program`→A19,
identificador→C01, `;`→B01, `:=`→B04, `:`→B03, `integer`→A16, `real`→A20,
constante inteira→C06), e `endFunction` reconhecida como palavra reservada (A07).

## Status
✅ Bloqueadores C1–C5 corrigidos. ✅ Médios M1 (truncagem), M3 (científico→realConst)
e M4 (`#` alias de `!=`) corrigidos. Pendências documentadas em `02-...`.
