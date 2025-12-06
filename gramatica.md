# Gramática Pascal Simplificado (Sem Ambiguidades)

## Regras de Produção

### Programa Principal

```
[PROGRAMA] → (program) [ID] (;) [CORPO]

[CORPO] → [DECLARACOES] (begin) [LISTA_COM] (end)
        | (begin) [LISTA_COM] (end)
```

### Declarações

```
[DECLARACOES] → [DEF_CONST] [DEF_TIPOS] [DEF_VAR] [LISTA_FUNC]
            | Є
            
[DEF_CONST] → (const) [LISTA_CONST]
            | Є

[DEF_TIPOS] → (type) [LISTA_TIPOS]
            | Є

[DEF_VAR] → (var) [LISTA_VAR]
          | Є
```

### Constantes

```
[LISTA_CONST] → [CONSTANTE] [LISTA_CONST']

[LISTA_CONST'] → [LISTA_CONST]
               | Є

[CONSTANTE] → [ID] (:=) [CONST_VALOR] (;)

[CONST_VALOR] → (") sequência alfanumérica (")
              | [EXP_MAT]
```

### Tipos

```
[LISTA_TIPOS] → [TIPO] [LISTA_TIPOS']

[LISTA_TIPOS'] → (;) [LISTA_TIPOS]
               | Є

[TIPO] → [ID] (:=) [TIPO_DADO]

[TIPO_DADO] → (integer)
            | (real)
            | (array) ([) [NUMERO] (]) (of) [TIPO_DADO]
            | (record) [LISTA_VAR] (end)
            | [ID]
```

### Variáveis

```
[LISTA_VAR] → [VARIAVEL] [LISTA_VAR']

[LISTA_VAR'] → (;) [LISTA_VAR]
             | Є

[VARIAVEL] → [LISTA_ID] (:) [TIPO_DADO]

[LISTA_ID] → [ID] [LISTA_ID']

[LISTA_ID'] → (,) [LISTA_ID]
            | Є
```

### Funções

```
[LISTA_FUNC] → [FUNCAO] [LISTA_FUNC]
             | Є

[FUNCAO] → [NOME_FUNCAO] [BLOCO_FUNCAO]

[NOME_FUNCAO] → (function) [ID] (() [LIST_VAR] ()) (:) [TIPO_DADO]

[BLOCO_FUNCAO] → [DEF_VAR] [BLOCO]

[BLOCO] → (begin) [LISTA_COM] (end)
```

### Comandos

```
[LISTA_COM] → [COMANDO] (;) [LISTA_COM]
            | Є

[COMANDO] → [ID] (:=) [VALOR]
          | [NOME] (:=) [VALOR]
          | (while) [EXP_LOGICA] [BLOCO]
          | (if) [EXP_LOGICA] (then) [BLOCO] [ELSE]
          | (write) [CONST_VALOR]
          | (read) [ID]

[ELSE] → (else) [BLOCO]
       | Є
```

### Valores e Nomes

```
[VALOR] → [ID] [VALOR']
        | [NUMERO]

[VALOR'] → [LISTA_NOME]
         | [EXP_MAT']

[NOME] → [ID] [NOME]
       | [NUMERO]

[LISTA_NOME] → (() [LISTA_NOME'] ())

[LISTA_NOME'] → [ID] [NOME]
              | [NUMERO]
              | (,) [LISTA_NOME]
              | Є
```

### Expressões Lógicas

```
[EXP_LOGICA] → [EXP_MAT] [EXP_LOGICA']

[EXP_LOGICA'] → [OP_LOGICO] [EXP_LOGICA]
              | Є

[OP_LOGICO] → (>) | (<) | (=) | (!)
```

### Expressões Matemáticas

```
[EXP_MAT] → [ID] [NOME] [EXP_MAT']
          | [NUMERO] [EXP_MAT']

[EXP_MAT'] → [OP_MAT] [EXP_MAT]
           | Є

[OP_MAT] → (+) | (-) | (*) | (/)
```

### Acesso a Membros

```
[NOME] → (.) [ID] [NOME]
       | ([) [ID] (]) [NOME]
       | ([) [NUMERO] (]) [NOME]
       | Є
```

## Tokens Léxicos

```
[ID] → Sequência alfanumérica iniciada por char (tratado no léxico)

[NUMERO] → Sequência de dígitos com a ocorrência de no máximo um ponto (tratado no léxico)
```

## Palavras Reservadas

- `program`
- `begin`
- `end`
- `const`
- `type`
- `var`
- `function`
- `while`
- `if`
- `then`
- `else`
- `write`
- `read`
- `integer`
- `real`
- `array`
- `of`
- `record`

## Símbolos Especiais

- `;` (ponto e vírgula)
- `:` (dois pontos)
- `:=` (atribuição)
- `,` (vírgula)
- `.` (ponto)
- `(` `)` (parênteses)
- `[` `]` (colchetes)
- `"` (aspas duplas)
- `+` `-` `*` `/` (operadores matemáticos)
- `>` `<` `=` `!` (operadores lógicos)
