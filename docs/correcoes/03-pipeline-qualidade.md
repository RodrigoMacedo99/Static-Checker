# Pipeline de qualidade (.claude) — resultado e ações

As correções passaram pelos agentes de qualidade definidos em `.claude/agents`:
`code-reviewer`, `test-architect` e `security-auditor`. Resultado inicial:
**aprovado com ressalvas**. Abaixo, cada ressalva e o que foi feito.

## Gates técnicos (estado final)
- ✅ **Testes**: 64 passam (`python -m pytest`).
- ✅ **Cobertura**: 97.45% (mínimo 80% em `pyproject.toml`).
- ✅ **Typecheck**: `python -m mypy src` — sem erros (mypy strict).
- ✅ **Security scan**: sem dependências de terceiros (`dependencies = []`).
- ⚪ **Lint**: não há linter configurado no projeto (sem ruff/flake8/CI).

## Ressalvas tratadas

### 🔴 Segurança (ALTO) — recursão no `Lexer` → estouro de pilha
`lexer.next_token` chamava a si mesma ao filtrar cada caractere inválido; com
~20k inválidos consecutivos dava `RecursionError`. **Corrigido**: convertido em
laço `while`. Teste de regressão: `test_invalid_char_does_not_break_or_recurse`
(5000 caracteres inválidos).

### 🔴 Bug encontrado pelos testes — `<=` e `>=`
Ao adicionar os testes dos operadores relacionais, descobriu-se que `<` e `>`
haviam sido colocados no mapa de símbolos de um caractere, fazendo `<=`/`>=`
serem lidos como `<` + `=` (filtrado). **Corrigido** em `symbol_recognizer.py`;
testes `test_relational_operators` cobrem `==`, `<`, `<=`, `>`, `>=`.

### 🟡 Testes — gaps de cobertura
- **E2E golden**: criado `tests/test_e2e_reports.py` — roda o pipeline completo
  (fonte → Lexer → Service → writers) e compara as linhas de detalhe do `.LEX`
  e as entradas do `.TAB`.
- **Operadores relacionais e `!` isolado**: adicionados em `test_lexer.py`.
- Novos testes de `string`/`char`, `FileReader`, `DoubleBuffer`, `ScopeManager`
  e `StaticCheckerService` (`test_string_char_recognizer.py`, `test_reports.py`,
  `test_io_and_service.py`).

### 🟡 Segurança (BAIXO) — encoding/IO
`FileReader.open` agora captura `OSError`/`UnicodeDecodeError` e relança como
`SourceReadException` (subclasse de `LexException`), evitando traceback bruto.
Removido o leitor de fonte morto em `main.py` e o parâmetro `source_content`
não usado em `LexReportWriter`.

## Ressalvas que são DECISÃO da equipe (não corrigidas no código)

### C1 — Conteúdo de string/char em CAIXA ALTA
O `truncate` coloca o lexema em caixa alta, o que também afeta o **conteúdo** de
`"strings"` e `'c'`. O `code-reviewer` apontou como perda de informação.

**Decisão:** mantido o comportamento **literal da especificação**, que determina
que *"todos os lexemes devem ser internamente convertidos para caixa alta antes
do processo de reconhecimento léxico **e armazenamento na tabela de símbolos**"*.
Como o projeto é avaliado contra essa especificação, optou-se por segui-la ao
pé da letra. **Questão omissa a confirmar com o professor**: se o conteúdo de
literais string/char deve preservar a caixa original, basta usar uma variante de
`truncate` sem `upper()` nos reconhecedores de string/char.

### M3 — Dados de contato (e-mail/telefone)
`src/shared/constants/__init__.py` (`COMPONENTS`) tem **placeholders**. A equipe
deve preencher e-mails e telefones reais antes da entrega (exigência do cabeçalho
dos relatórios). Não é um problema de código.

## Pendência opcional
- Adicionar **CI** (GitHub Actions) + **ruff** para tornar a pipeline automática
  (lint + typecheck + test + coverage) — hoje os checks são executados
  manualmente.
