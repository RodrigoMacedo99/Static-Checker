# Correções aplicadas

Cada item descreve **o que** foi corrigido, **por que** (referência à
especificação) e **onde** (arquivos). Os testes em `tests/` foram atualizados
para validar o comportamento correto.

---

## C1 — Códigos de átomo conforme o Apêndice A
**Problema.** `atom_code.py` usava um esquema inventado (identificadores em A01,
reservadas em B01–B26, símbolos em C01–C24). A especificação (Apêndice A) e o
exemplo oficial exigem outro mapeamento.

**Por quê.** Os relatórios `.LEX`/`.TAB` precisam emitir exatamente os códigos do
Apêndice A; o exemplo da spec mostra `VAR1→C01`, `;→B01`, `:=→B04`, `[→B08`,
`REAL→A20`. Com os códigos errados, a entrega é reprovada.

**Correção.** Reescrita de `AtomCode`:
- Palavras reservadas → **A01–A26** (boolean=A01 … while=A26)
- Símbolos reservados → **B01–B22** (`;`=B01 … `>=`=B22)
- Identificadores/constantes → **C01–C07** (variable=C01, functionName=C02,
  programName=C03, stringConst=C04, charConst=C05, intConst=C06, realConst=C07)
- `EOF` passou a usar o valor `"EOF"` (antes `D01`, que no Apêndice A é reservado
  para submáquinas).

**Arquivos.** `src/domain/token/atom_code.py`, `reserved_words_table.py`,
`token_factory.py`, `token.py`, `number_recognizer.py`, `symbol_recognizer.py`,
`static_checker_service.py`.

| Lexeme | Antes | Depois (oficial) |
|---|---|---|
| identificador | A01 | **C01** |
| `program` | B01 | **A19** |
| `integer` | B11 | **A16** |
| `:` | C02 | **B03** |
| `;` | C03 | **B01** |
| `:=` | C01 | **B04** |

---

## C2 — Sensibilidade a maiúsculas (case-insensitive) corrigida
**Problema.** Os reconhecedores só aceitavam **minúsculas**
(`can_handle` usava `ch.islower()`; conjuntos de chars só com `a–z`), e havia um
hack para a letra `I`/`If`. Um fonte em maiúsculas (`PROGRAM Teste`) quebrava.

**Por quê.** A especificação (seção *Analisador léxico*) determina que todos os
lexemes sejam tratados em **CAIXA ALTA** e que maiúsculas/minúsculas sejam
equivalentes.

**Correção.**
- `IdentifierRecognizer.can_handle` → `ch.isalpha() or ch == "_"`.
- Conjuntos de chars de string/char passam a aceitar `A–Z` e `a–z`.
- Exponencial de número aceita `e`/`E`.
- Lexemes são armazenados em caixa alta (já via `truncate`).
- Removido o hack do `I`/`If`: `if`/`IF`/`If` resolvem para **A15** pela tabela
  de reservadas (lookup case-insensitive).

**Arquivos.** `identifier_recognizer.py`, `string_recognizer.py`,
`char_recognizer.py`, `number_recognizer.py`, `symbol_recognizer.py`.

---

## C3 — Palavra reservada `endFunction` (A07) adicionada
**Problema.** A tabela de reservadas tinha `endFunctions` mas **não**
`endFunction` (singular). Resultado: `endFunction` virava identificador na tabela
de símbolos.

**Por quê.** O Apêndice A define os dois átomos distintos: `endFunction` (A07) e
`endFunctions` (A08).

**Correção.** Adicionada a entrada `"ENDFUNCTION": AtomCode.END_FUNCTION`.

**Arquivo.** `reserved_words_table.py`.

---

## C4 — Fim do uso indevido de `EOF` como char inválido
**Problema.** O `SymbolRecognizer` retornava `AtomCode.EOF` para `=`, `!`, `I`
isolados e para chars desconhecidos, injetando **tokens-EOF espúrios** no fluxo.

**Por quê.** Char inválido deve ser **filtrado** (filtro de 1º nível): descartado
sem gerar token e sem encerrar a análise. Só o real fim de arquivo encerra.

**Correção.** `recognize` agora pode retornar `Optional[Token]`; quando o trecho
é inválido (`=` ou `!` isolados), retorna `None` e o `Lexer` simplesmente
continua. `can_handle` do `SymbolRecognizer` foi restringido ao conjunto exato de
caracteres que iniciam símbolos válidos.

**Arquivos.** `token_recognizer.py` (assinatura), `lexer.py` (trata `None`),
`symbol_recognizer.py`.

---

## C5 — Relatórios `.LEX` e `.TAB` no formato da especificação
**Problema.** O `.LEX` não imprimia o `indiceTabSimb` por linha e o cabeçalho não
tinha e-mail/telefone nem o título exato; o `.TAB` não imprimia
`QtdCharsAntesTrunc`/`QtdCharDepoisTrunc`.

**Por quê.** A seção *Saídas* define o conteúdo mínimo obrigatório dos dois
relatórios.

**Correção.** Reescrita dos dois writers seguindo o exemplo oficial:
- Cabeçalho: `Código da Equipe`, `Componentes:` (nome; e-mail; telefone),
  título `RELATÓRIO DA ANÁLISE LÉXICA.` / `RELATÓRIO DA TABELA DE SÍMBOLOS.` e
  `Texto fonte analisado: <nome>.261`.
- `.LEX`: `Lexeme: X, Código: Y, indiceTabSimb: Z, Linha: W.`
- `.TAB`: `Entrada/Código/Lexeme` + `QtdCharsAntesTrunc/QtdCharDepoisTrunc` +
  `TipoSimb/Linhas`.

**Arquivos.** `lex_report_writer.py`, `tab_report_writer.py`,
`shared/constants/__init__.py` (lista `COMPONENTS`).

> ⚠️ Os e-mails e telefones em `COMPONENTS` são **placeholders** — a equipe deve
> preencher os dados reais antes da entrega.

---

## M1 — Truncagem de 30 caracteres em todos os átomos
**Problema.** Só identificadores eram truncados a 30 chars.

**Por quê.** A spec limita **qualquer** átomo a 30 caracteres válidos (aspas
contam para strings/chars).

**Correção.** Number/String/Char passam a usar `truncate()` e registram
`QtdCharsAntesTrunc`/`QtdCharDepoisTrunc`.

**Arquivos.** `number_recognizer.py`, `string_recognizer.py`, `char_recognizer.py`.

---

## M3 — Notação científica classificada como `realConst` (C07)
**Problema.** Existia um átomo separado `SCIENTIFIC_LIT`.

**Por quê.** O Apêndice A só define `intConst` (C06) e `realConst` (C07); a forma
exponencial faz parte do padrão de `realConst`.

**Correção.** O autômato N0–N6 continua igual, mas os estados 3 e 6 (real e
científico) mapeiam para **C07**; o estado 1 (inteiro) mapeia para **C06**.

**Arquivo.** `number_recognizer.py`.

---

## M4 — `#` como alias de `!=` (B18)
**Problema.** `#` tinha código próprio, separado de `!=`.

**Por quê.** O Apêndice A define `#` como **alias de `!=`** (mesmo código B18).

**Correção.** `#` mapeia para `AtomCode.NEQ` (B18).

**Arquivo.** `symbol_recognizer.py`.

---

## Ajuste relacionado — constantes na tabela de símbolos e contagem de linhas
- **Constantes armazenadas.** Pela categoria *Identificadores* do Apêndice A
  (C04–C07) e pela seção *TipoSimb*, `intConst`/`realConst`/`stringConst`/
  `charConst` também vão para a tabela de símbolos, com tipo intrínseco
  (IN/FP/ST/CH). Implementado injetando a `SymbolTable` nos reconhecedores de
  number/string/char (`main.py`).
- **Linhas com repetição.** A spec pede as linhas das **primeiras 5 ocorrências**
  (ex.: `VAR1 → (1, 2, 2, 2, 3)`). Removida a deduplicação em
  `SymbolEntry.add_line`.
