# Decisões de projeto e pendências

## Decisões / simplificações conscientes

### Identificadores emitidos como `variable` (C01)
O Apêndice A separa `variable` (C01), `functionName` (C02) e `programName`
(C03). **Lexicamente os três são idênticos** (mesmo padrão de formação); só é
possível distingui-los com **contexto sintático** (ex.: o nome após `program` é
programName; após `funcType Type :` é functionName). Como esta entrega cobre só a
análise léxica, todos os identificadores são emitidos como **C01**, exatamente
como no exemplo oficial da especificação. A distinção C02/C03 fica para a fase
sintática futura.

### Inferência de `TipoSimb` é best-effort
O `StaticCheckerService` preenche o tipo dos identificadores declarados
(`varType Type : ...` → IN/FP/ST/CH/BL/VD; `[]` → tipos array AI/AF/...). É uma
heurística baseada na ordem dos tokens, suficiente para os relatórios desta
etapa, não uma análise sintática completa. Constantes recebem tipo intrínseco
no momento do reconhecimento (intConst→IN, realConst→FP, stringConst→ST,
charConst→CH).

### `DoubleBuffer` é in-memory
A implementação carrega o arquivo inteiro em memória, expondo a interface
`CharStream`. A especificação **não exige** buffer de duas metades ("embora não
seja exigido"). O documento de arquitetura (`EQ01PROJ`) descreve o buffer
clássico de duas metades — é uma divergência doc×código a reconciliar (ver
pendências), sem impacto funcional.

### E-mails e telefones são placeholders
`src/shared/constants/__init__.py` (`COMPONENTS`) traz dados de contato fictícios.
A especificação exige nome + e-mail + telefone reais de cada componente no
cabeçalho dos relatórios. **A equipe deve preencher antes da entrega.**

---

## Pendências (não bloqueantes para a Etapa 7)

- **M2 — Distinção C02/C03**: implementar na fase sintática (functionName /
  programName).
- **M5 — Reconciliar arquitetura × código** (`EQ01PROJ`): a pasta
  `domain/lexer/automaton/` descrita no documento não existe; os relatórios são
  `*ReportWriter` (não Builders com `self` encadeado); `Lexer.next_token` retorna
  `Token`/`None` em vez de `Result[Token, LexError]`. Decidir entre ajustar o
  documento ou o código.
- **Golden files de integração**: criar `.LEX`/`.TAB` esperados (ex.: a partir do
  `Teste.261` do exemplo oficial) e um teste que compara a saída — prometido no
  PROJ (seção 9.4) e ainda ausente.
- **Conversão dos PDFs com Docling**: o Docling não pôde ser instalado neste
  ambiente (provável incompatibilidade do Python 3.13 com os wheels de torch).
  As conversões em Markdown foram feitas por extração direta e estão no vault
  Obsidian (`Static-Checker/PDFs-Convertidos/`).

---

## Resumo da validação por autômato (após correções)

| Autômato (BRUT/OTIM) | Reconhecedor | Situação |
|---|---|---|
| Identifier ID0→ID1 | `identifier_recognizer` | ✅ equivalente, case-insensitive |
| Number N0–N6 | `number_recognizer` | ✅ fiel; truncagem + C06/C07 |
| StringLiteral SL0→SL3 | `string_recognizer` | ✅ rejeita vazio; truncagem; C04 |
| CharacterLiteral CH0→CH3 | `char_recognizer` | ✅ só letra; C05 |
| RelOp/Add/Mul/símbolos | `symbol_recognizer` | ✅ códigos B*, `#`=`!=`, filtro de inválidos |
