# Documentação Técnica - Analisador Léxico

## Implementação

O analisador léxico foi implementado usando a biblioteca **PLY (Python Lex-Yacc)**, seguindo as orientações dos slides do professor e a gramática Pascal Simplificado.

## Estrutura do Código

### 1. Definição de Tokens

```python
tokens = (
    'PROGRAM', 'BEGIN', 'END', 'CONST', 'TYPE', 'VAR',
    'FUNCTION', 'WHILE', 'IF', 'THEN', 'ELSE',
    'WRITE', 'READ', 'INTEGER', 'REAL', 'ARRAY',
    'OF', 'RECORD', 'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'GT', 'LT', 'EQUALS', 'EXCLAMATION',
    'ASSIGN', 'SEMICOLON', 'COLON', 'COMMA',
    'DOT', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET'
)
```

### 2. Palavras Reservadas

As palavras reservadas são tratadas com prioridade sobre identificadores através de um dicionário:

```python
reserved = {
    'program': 'PROGRAM',
    'begin': 'BEGIN',
    # ... outras palavras
}
```

Quando um identificador é reconhecido, o lexer verifica se ele está no dicionário de palavras reservadas.

### 3. Tokens Simples (Expressões Regulares Diretas)

Símbolos especiais e operadores são definidos como variáveis com prefixo `t_`:

```python
t_PLUS = r'\+'
t_SEMICOLON = r';'
t_ASSIGN = r':='
```

### 4. Tokens Complexos (Funções)

Tokens que requerem processamento adicional são implementados como funções:

#### Números
```python
def t_NUMBER(t):
    r'\d+\.?\d*|\d*\.\d+'
```
- Reconhece inteiros e reais
- Permite no máximo um ponto decimal
- Converte o valor para int ou float

#### Strings
```python
def t_STRING(t):
    r'"[^"]*"'
```
- Reconhece sequências entre aspas duplas
- Remove as aspas do valor armazenado

#### Identificadores
```python
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
```
- Começa com letra
- Pode conter letras, dígitos e underscores
- Verifica se é palavra reservada

#### Comentários
```python
def t_COMMENT(t):
    r'\{[^}]*\}'
```
- Texto entre chaves `{ }`
- São descartados (não geram tokens)

### 5. Controle de Linha

```python
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
```

Mantém o contador de linhas atualizado para relatórios de erro.

### 6. Caracteres Ignorados

```python
t_ignore = ' \t'
```

Espaços e tabulações são automaticamente ignorados.

### 7. Tratamento de Erros

```python
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)
```

Quando um caractere não pode ser classificado:
- Imprime mensagem de erro com o caractere e linha
- Pula o caractere e continua a análise

## Prioridade de Regras no PLY

O PLY resolve conflitos de regras seguindo estas prioridades:

1. **Maior sequência**: Escolhe a regra que casa com a maior sequência de caracteres
2. **Ordem de definição**: Em caso de empate, escolhe a primeira regra definida no código

Por isso:
- Palavras reservadas são verificadas antes de identificadores
- Tokens complexos (funções) têm prioridade sobre tokens simples
- `:=` é reconhecido antes de `:` (pela maior sequência)

## Fluxo de Processamento

1. **Inicialização**: `lexer = lex.lex()`
2. **Entrada**: `lexer.input(codigo)`
3. **Tokenização**: Loop chamando `lexer.token()` até retornar `None`
4. **Saída**: Cada token contém:
   - `type`: Tipo do token (ex: 'ID', 'NUMBER')
   - `value`: Valor/lexema do token
   - `lineno`: Número da linha
   - `lexpos`: Posição no buffer

## Exemplos de Reconhecimento

### Identificadores vs Palavras Reservadas
```
while    → WHILE (palavra reservada)
wile     → ID (identificador, erro de digitação)
while2   → ID (identificador)
_while   → ID (identificador)
```

### Números
```
123      → NUMBER (int: 123)
12.3     → NUMBER (float: 12.3)
.789     → NUMBER (float: 0.789)
12.3.4   → NUMBER, DOT, NUMBER (erro: dois pontos)
```

### Operadores
```
:=       → ASSIGN
:        → COLON
=        → EQUALS
==       → EQUALS, EQUALS (dois tokens)
```

### Comentários
```
{ comentario }           → ignorado
{ comentario { aninhado} → não suportado (erro)
```

## Limitações e Observações

1. **Comentários aninhados**: Não são suportados
2. **Strings multi-linha**: Não são suportadas
3. **Escape em strings**: Não há suporte para `\"` ou `\n`
4. **Case-insensitive**: Palavras reservadas são case-insensitive (`BEGIN` = `begin`)
5. **Números**: Formato livre de pontos (`.789` e `345.` são válidos)

## Testes Realizados

### Teste 1: Programa Simples ✓
- Palavras reservadas
- Declarações de variáveis
- Comandos básicos
- Expressões simples

### Teste 2: Programa Completo ✓
- Constantes e tipos
- Arrays e records
- Funções com parâmetros
- Laços e condicionais
- Comentários

### Teste 3: Detecção de Erros ✓
- Caracteres ilegais (`@`, `#`, etc)
- Tokens malformados
- Continua após erro

## Performance

O PLY gera um autômato finito determinístico (DFA) otimizado:
- Primeira execução: ~100ms (geração do DFA)
- Execuções seguintes: ~10ms (DFA em cache)
- Arquivo `parser.out`: Tabela de estados gerada

## Referências

- Slides do professor sobre análise léxica
- Slides sobre algoritmo de análise léxica
- Slides sobre PLY (Python Lex-Yacc)
- Documentação oficial do PLY
- Gramática Pascal Simplificado (gramatica.md)
