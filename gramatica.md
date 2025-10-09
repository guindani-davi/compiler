# Especificação do Compilador

## Classificação de Tokens

### 1. Palavras-reservadas
`program`, `const`, `type`, `var`, `begin`, `end`, `function`, `of`, `record`, `array`, `integer`, `real`, `while`, `if`, `then`, `else`, `write`, `read`

### 2. Identificadores
- Padrão: `[A-Za-z][A-Za-z0-9_]*`
- Exemplos: `funcoes`, `TAM`, `aluno`

### 3. Números
- **Inteiro**: `0|[1-9][0-9]*`
- **Real**: `[0-9]+\.[0-9]+`

### 4. Strings
- Padrão: `"([^"\n]|"")*"`
- Exemplo: `"digite as notas do aluno"`

### 5. Operadores
`:=`, `+`, `-`, `*`, `/`, `=`, `<>`, `<`, `<=`, `>`, `>=`

### 6. Delimitadores
`(`, `)`, `[`, `]`, `;`, `:`, `,`, `.`

### 7. Comentários
- `//` até fim da linha
- `{ ... }`
- `(* ... *)`

## Gramática
PROGRAMA ::= 'program' ID ';' CORPO

CORPO ::= DECLARACOES 'begin' LISTA_COM 'end' 
        | 'begin' LISTA_COM 'end'

DECLARACOES ::= DEF_CONST DEF_TIPOS DEF_VAR LISTA_FUNC 
              | ε

DEF_CONST ::= 'const' LISTA_CONST 
            | ε

LISTA_CONST ::= CONSTANTE (CONSTANTE)*

CONSTANTE ::= ID ':=' CONST_VALOR ';'

CONST_VALOR ::= STR | EXP_MAT

DEF_TIPOS ::= 'type' LISTA_TIPOS 
            | ε

LISTA_TIPOS ::= TIPO (';' TIPO)*

TIPO ::= ID ':=' TIPO_DADO

TIPO_DADO ::= 'integer' 
            | 'real' 
            | 'array' '[' NUM ']' 'of' TIPO_DADO 
            | 'record' LISTA_VAR 'end' 
            | ID

DEF_VAR ::= 'var' LISTA_VAR 
          | ε

LISTA_VAR ::= VARIAVEL (';' VARIAVEL)*

VARIAVEL ::= LISTA_ID ':' TIPO_DADO

LISTA_ID ::= ID (',' ID)*

FUNCAO ::= 'function' ID '(' PARAM_FORM? ')' ':' TIPO_DADO BLOCO_FUNCAO

PARAM_FORM ::= PARAM (',' PARAM)*

PARAM ::= LISTA_ID ':' TIPO_DADO

BLOCO_FUNCAO ::= DEF_VAR BLOCO 
               | BLOCO

BLOCO ::= 'begin' LISTA_COM 'end' 
        | COMANDO

LISTA_COM ::= COMANDO (';' COMANDO)*

COMANDO ::= NOME ':=' VALOR 
          | 'while' EXP_LOGICA BLOCO 
          | 'if' EXP_LOGICA 'then' BLOCO ELSE_OPT 
          | 'write' '(' (EXP_MAT|STR) ')' 
          | 'read' '(' NOME ')' 
          | BLOCO

ELSE_OPT ::= 'else' BLOCO 
           | ε

VALOR ::= EXP_MAT 
        | ID LISTA_ARG?

LISTA_ARG ::= '(' LISTA_EXP? ')'

LISTA_EXP ::= EXP_MAT (',' EXP_MAT)*

EXP_LOGICA ::= EXP_REL

EXP_REL ::= EXP_MAT (OP_REL EXP_MAT)?

OP_REL ::= '=' | '<>' | '<' | '<=' | '>' | '>='

EXP_MAT ::= TERMO (( '+' | '-' ) TERMO)*

TERMO ::= FATOR (( '*' | '/' ) FATOR)*

FATOR ::= PARAMETRO 
        | '(' EXP_MAT ')'

PARAMETRO ::= NOME | NUM

NOME ::= ID ('.' ID | '[' EXP_MAT ']')*