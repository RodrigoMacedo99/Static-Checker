# Static-Checker
Analisador léxico para a linguagem BobEnzo2026-1 (projeto educacional).

## Visão geral

Este repositório contém um verificador estático (lexer + checagem de símbolos) capaz de ler um arquivo-fonte da linguagem BobEnzo2026-1 e gerar relatórios léxicos e de tabela de símbolos.

## Requisitos

- Python 3.11 ou superior
- Dependências: nenhuma externa (projeto usa apenas stdlib)

As configurações de teste e verificação estão em `pyproject.toml`.

## Executando o analisador

1. Abra um terminal na raiz do projeto.
2. Passe o nome base do arquivo (sem extensão) como argumento para o script `run.py`.

Exemplo usando o exemplo completo fornecido:

```
python run.py bobenzo_examples_cods\\exemplo_completo
```

Observações:
- O programa espera apenas o nome-base do arquivo (por exemplo `exemplo_completo`) e automaticamente usa a extensão esperada (definida em `src/shared/constants`).
- Ao finalizar com sucesso, serão criados dois arquivos de relatório: um relatório léxico (`*.LEX`) e uma tabela de símbolos (`*.TAB`).

## Estrutura do projeto (resumida)

- `run.py` — ponto de entrada (wrapper simples)
- `src/main.py` — composição e orquestração do serviço
- `src/domain/lexer` — implementação do analisador léxico e reconhecedores
- `src/domain/symbol_table` — tabela de símbolos e tipos
- `src/infrastructure/reports` — geradores de relatório (`lex`, `tab`)
- `tests/` — testes unitários com `pytest`

## Executando testes

Execute os testes com `pytest` (recomendado via módulo):

```
python -m pytest
```

Os parâmetros de `pytest` e `coverage` estão definidos em `pyproject.toml`.

## Saída esperada

Em execução com sucesso, você verá no terminal uma mensagem como:

```
OK — 123 tokens, 45 símbolos.
	exemplo_completo.LEX e exemplo_completo.TAB gerados.
```

Em caso de erro léxico, o programa imprime a mensagem no `stderr` e retorna código de saída `1`.

## Contribuição e contato

Sugestões, issues e PRs são bem-vindos. Abra uma issue no repositório para relatar bugs ou propor melhorias.

---
Arquivo gerado automaticamente pelo assistente — confirme se quer que eu rode os testes agora.

## Instalação rápida para usuários leigos (Windows)

Se você não é desenvolvedor, siga estes passos simples para preparar o ambiente e executar o analisador.

1. Instalar o Python 3.11+:
	- Acesse https://www.python.org/downloads/windows/ e baixe o instalador para Windows.
	- Execute o instalador e marque a opção "Add Python to PATH" antes de clicar em "Install Now".

2. Verificar instalação (Abra o PowerShell ou Prompt de Comando):

```
python --version
python -m pip --version
```

3. Atualizar o pip (opcional, recomendado):

```
python -m pip install --upgrade pip
```

4. Instalar o montador/runner `uv` (se você quiser usar o comando `uv run` mostrado nos exemplos):

```
python -m pip install uv
```

Observação: se a instalação do `uv` falhar, não se preocupe — você pode rodar o programa diretamente com `python` (passo 6).

5. Executar o analisador usando `uv` (exemplo):

```
uv run run.py bobenzo_examples_cods\exemplo_completo
```

Também funciona passando o caminho com extensão (ex.: `.261`):

```
uv run run.py .\bobenzo_examples_cods\exemplo_completo.261
```

6. Instalar dependências do projeto e alternativa simples (sem `uv`):

- (Recomendado) Criar e ativar um ambiente virtual (Windows PowerShell):

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- Instalar as dependências e o próprio projeto a partir do `pyproject.toml`:

```
python -m pip install --upgrade pip
python -m pip install -e .
```

OBS: se o projeto não declarar dependências externas, os comandos acima não instalarão pacotes extras, mas ainda preparam o ambiente para execução.

- Alternativa simples sem instalar `uv` (ou sem criar venv):

```
python run.py bobenzo_examples_cods\exemplo_completo
```

7. Resultado esperado:
	- No terminal: mensagem informando número de tokens e símbolos.
	- Arquivos gerados na mesma pasta do projeto: `*.LEX` e `*.TAB`.

Se quiser, eu posso executar os testes do projeto para verificar tudo agora. Responda "Sim" que eu rodo `python -m pytest`.
