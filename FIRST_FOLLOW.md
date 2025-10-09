# Conjuntos FIRST e FOLLOW da Gramática SimplePascal

## Conjuntos FIRST

### Não-terminais principais:
- **FIRST(PROGRAMA)** = { `program` }
- **FIRST(CORPO)** = { `const`, `type`, `var`, `function`, `begin` }
- **FIRST(DECLARACOES)** = { `const`, `type`, `var`, `function`, ε }
- **FIRST(DEF_CONST)** = { `const`, ε }
- **FIRST(LISTA_CONST)** = { ID }
- **FIRST(CONSTANTE)** = { ID }
- **FIRST(CONST_VALOR)** = { STRING, ID, NUM_INT, NUM_REAL, `(` }

### Definição de tipos:
- **FIRST(DEF_TIPOS)** = { `type`, ε }
- **FIRST(LISTA_TIPOS)** = { ID }
- **FIRST(TIPO)** = { ID }
- **FIRST(TIPO_DADO)** = { `integer`, `real`, `array`, `record`, ID }

### Definição de variáveis:
- **FIRST(DEF_VAR)** = { `var`, ε }
- **FIRST(LISTA_VAR)** = { ID }
- **FIRST(VARIAVEL)** = { ID }
- **FIRST(LISTA_ID)** = { ID }

### Funções:
- **FIRST(LISTA_FUNC)** = { `function`, ε }
- **FIRST(FUNCAO)** = { `function` }
- **FIRST(PARAM_FORM)** = { ID, ε }
- **FIRST(PARAM)** = { ID }
- **FIRST(BLOCO_FUNCAO)** = { `var`, `begin`, ID, `while`, `if`, `write`, `read` }
- **FIRST(BLOCO)** = { `begin`, ID, `while`, `if`, `write`, `read` }

### Comandos:
- **FIRST(LISTA_COM)** = { ID, `while`, `if`, `write`, `read`, `begin` }
- **FIRST(COMANDO)** = { ID, `while`, `if`, `write`, `read`, `begin` }
- **FIRST(ELSE_OPT)** = { `else`, ε }

### Valores e expressões:
- **FIRST(VALOR)** = { ID, NUM_INT, NUM_REAL, `(` }
- **FIRST(LISTA_ARG)** = { `(` }
- **FIRST(LISTA_EXP)** = { ID, NUM_INT, NUM_REAL, `(`, ε }
- **FIRST(EXP_LOGICA)** = { ID, NUM_INT, NUM_REAL, `(` }
- **FIRST(EXP_REL)** = { ID, NUM_INT, NUM_REAL, `(` }
- **FIRST(OP_REL)** = { `=`, `<>`, `<`, `<=`, `>`, `>=` }
- **FIRST(EXP_MAT)** = { ID, NUM_INT, NUM_REAL, `(` }
- **FIRST(TERMO)** = { ID, NUM_INT, NUM_REAL, `(` }
- **FIRST(FATOR)** = { ID, NUM_INT, NUM_REAL, `(` }
- **FIRST(PARAMETRO)** = { ID, NUM_INT, NUM_REAL }
- **FIRST(NOME)** = { ID }

## Conjuntos FOLLOW

### Não-terminais principais:
- **FOLLOW(PROGRAMA)** = { $ }
- **FOLLOW(CORPO)** = { $ }
- **FOLLOW(DECLARACOES)** = { `begin` }
- **FOLLOW(DEF_CONST)** = { `type`, `var`, `function`, `begin` }
- **FOLLOW(LISTA_CONST)** = { `type`, `var`, `function`, `begin` }
- **FOLLOW(CONSTANTE)** = { ID, `type`, `var`, `function`, `begin` }
- **FOLLOW(CONST_VALOR)** = { `;` }

### Definição de tipos:
- **FOLLOW(DEF_TIPOS)** = { `var`, `function`, `begin` }
- **FOLLOW(LISTA_TIPOS)** = { `var`, `function`, `begin` }
- **FOLLOW(TIPO)** = { `;`, `var`, `function`, `begin` }
- **FOLLOW(TIPO_DADO)** = { `;`, `end`, `var`, `function`, `begin` }

### Definição de variáveis:
- **FOLLOW(DEF_VAR)** = { `function`, `begin`, `end` }
- **FOLLOW(LISTA_VAR)** = { `function`, `begin`, `end` }
- **FOLLOW(VARIAVEL)** = { `;`, `function`, `begin`, `end` }
- **FOLLOW(LISTA_ID)** = { `:` }

### Funções:
- **FOLLOW(LISTA_FUNC)** = { `begin` }
- **FOLLOW(FUNCAO)** = { `function`, `begin` }
- **FOLLOW(PARAM_FORM)** = { `)` }
- **FOLLOW(PARAM)** = { `,`, `)` }
- **FOLLOW(BLOCO_FUNCAO)** = { `function`, `begin` }
- **FOLLOW(BLOCO)** = { `else`, `;`, `function`, `begin`, `end` }

### Comandos:
- **FOLLOW(LISTA_COM)** = { `end` }
- **FOLLOW(COMANDO)** = { `;`, `end` }
- **FOLLOW(ELSE_OPT)** = { `;`, `end` }

### Valores e expressões:
- **FOLLOW(VALOR)** = { `;`, `,`, `)`, `end` }
- **FOLLOW(LISTA_ARG)** = { `;`, `,`, `)`, `end` }
- **FOLLOW(LISTA_EXP)** = { `)` }
- **FOLLOW(EXP_LOGICA)** = { `then`, `begin`, ID, `while`, `if`, `write`, `read` }
- **FOLLOW(EXP_REL)** = { `then`, `begin`, ID, `while`, `if`, `write`, `read` }
- **FOLLOW(OP_REL)** = { ID, NUM_INT, NUM_REAL, `(` }
- **FOLLOW(EXP_MAT)** = { `=`, `<>`, `<`, `<=`, `>`, `>=`, `;`, `,`, `)`, `]`, `then`, `begin`, `end` }
- **FOLLOW(TERMO)** = { `+`, `-`, `=`, `<>`, `<`, `<=`, `>`, `>=`, `;`, `,`, `)`, `]`, `then`, `begin`, `end` }
- **FOLLOW(FATOR)** = { `*`, `/`, `+`, `-`, `=`, `<>`, `<`, `<=`, `>`, `>=`, `;`, `,`, `)`, `]`, `then`, `begin`, `end` }
- **FOLLOW(PARAMETRO)** = { `*`, `/`, `+`, `-`, `=`, `<>`, `<`, `<=`, `>`, `>=`, `;`, `,`, `)`, `]`, `then`, `begin`, `end` }
- **FOLLOW(NOME)** = { `:=`, `*`, `/`, `+`, `-`, `=`, `<>`, `<`, `<=`, `>`, `>=`, `;`, `,`, `)`, `]`, `then`, `begin`, `end` }

## Notas sobre a Implementação

### PLY Yacc e Conjuntos FIRST/FOLLOW

O PLY (Python Lex-Yacc) **calcula automaticamente** os conjuntos FIRST e FOLLOW durante a construção da tabela de parsing. Por isso:

1. **Não é necessário implementar manualmente** o cálculo desses conjuntos
2. O PLY usa **parsing LR(1)**, que é mais poderoso que LL(1)
3. Conflitos shift/reduce são resolvidos automaticamente pelo PLY
4. Os conjuntos acima são documentação para entendimento da gramática

### Tratamento de Erros no PLY

O PLY oferece a função `p_error(p)` para tratamento de erros sintáticos:
- **p** contém informação sobre o token que causou o erro
- **p.lineno** contém o número da linha
- **p.value** contém o valor do token

### Recuperação de Erros

Para implementar recuperação de erros com PLY:
1. Use `parser.errok()` para resetar o estado de erro
2. Use `parser.restart()` para reiniciar o parsing
3. Implemente regras de sincronização baseadas nos conjuntos FOLLOW
