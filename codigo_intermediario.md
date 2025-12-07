# Geração de Código Intermediário

## Objetivo

Transformar a representação hierárquica (AST) em uma representação sequencial de código intermediário, simulando um programa para uma máquina abstrata.

### Vantagens

- **Adia decisões** relacionadas com características da máquina alvo:
  - Quantidade de registradores
  - Localização física das variáveis (memória ou registrador)
  - Endereçamento de funções/procedimentos

- **Facilita otimização**: Mais fácil otimizar código intermediário que código final

- **Portabilidade**: Linguagem intermediária entre a fonte e a final

## Formato: Código de 3 Endereços

Forma intermediária onde cada instrução possui **1 operador** e **no máximo 3 posições de memória** associados.

### Estrutura

```
OP | Endereço 1 | Endereço 2 | Endereço 3
```

### Conjunto de Instruções

| Operação | End. 1 (destino) | End. 2 (operando1) | End. 3 (operando2) | Descrição |
|----------|------------------|--------------------|--------------------|-----------|
| **MOV**  | destino          | origem             | -                  | Atribuição simples |
| **ADD**  | resultado        | operando1          | operando2          | Adição |
| **SUB**  | resultado        | operando1          | operando2          | Subtração |
| **MUL**  | resultado        | operando1          | operando2          | Multiplicação |
| **DIV**  | resultado        | operando1          | operando2          | Divisão |
| **GTR**  | resultado        | operando1          | operando2          | Maior que (>) |
| **LES**  | resultado        | operando1          | operando2          | Menor que (<) |
| **EQL**  | resultado        | operando1          | operando2          | Igual (=) |
| **NEQ**  | resultado        | operando1          | operando2          | Diferente (!) |
| **JMP**  | label            | -                  | -                  | Salto incondicional |
| **JNZ**  | label            | variável           | -                  | Salto se não-zero (verdadeiro) |
| **LBL**  | label            | -                  | -                  | Definição de label |
| **CALL** | função           | -                  | -                  | Chamada de função |
| **RET**  | valor            | -                  | -                  | Retorno de função |
| **PUSH** | valor            | -                  | -                  | Empilha parâmetro |
| **POP**  | destino          | -                  | -                  | Desempilha resultado |
| **READ** | variável         | -                  | -                  | Leitura de entrada |
| **WRITE**| valor            | -                  | -                  | Escrita de saída |

## Transformação de Sub-árvores

### Princípios

1. Cada sub-árvore é tratada individualmente
2. Percorrer a árvore em **pós-ordem** gerando código associado
3. Diferentes tipos de sub-árvore têm características diferentes:
   - **Declaração**: Reservar espaço de armazenamento
   - **Comando**: Criar labels para destino de saltos
   - **Expressão**: Criar variáveis temporárias para resultado

### Variáveis Temporárias

- Criadas durante processamento de expressões
- Formato: `TEMP1`, `TEMP2`, `TEMP3`, etc.
- Armazenam resultados intermediários de operações

### Labels

- Criadas para controle de fluxo (if, while)
- Formato: `LABEL1`, `LABEL2`, `LABEL3`, etc.
- Marcam destinos de saltos

## Padrões de Transformação

### 1. Expressões Aritméticas

**Regra**: `EXP -> PARM OP EXP`

```
# Código fonte
A + B

# Código intermediário
ADD TEMP1, A, B
```

**Regra**: `EXP -> PARM`

```
# Código fonte
A

# Código intermediário
MOV TEMP1, A
```

**Exemplo Completo**: `A + B * C`

```
# Árvore:
#     +
#    / \
#   A   *
#      / \
#     B   C

# Código intermediário:
MUL TEMP1, B, C    # Calcula B * C
ADD TEMP2, A, TEMP1 # Calcula A + TEMP1
```

### 2. Atribuição

**Regra**: `COM -> ID := EXP`

```
# Código fonte
A := B + C

# Código intermediário
ADD TEMP1, B, C
MOV A, TEMP1
```

### 3. Condicional Simples (IF-THEN)

**Regra**: `COM -> if EXP then BLC`

```
# Código fonte
if A > B then
    C := A
end

# Código intermediário
GTR TEMP1, A, B      # Avalia condição
JNZ LABEL_THEN, TEMP1  # Salta se verdadeiro
JMP LABEL1           # Condição falsa, pula o then
LBL LABEL_THEN       # Início do then
MOV C, A             # Bloco then
LBL LABEL1           # Fim do if
```

### 4. Condicional com ELSE (IF-THEN-ELSE)

**Regra**: `COM -> if EXP then BLC else BLC`

```
# Código fonte
if A > B then
    C := A
else
    C := B
end

# Código intermediário
GTR TEMP1, A, B       # Avalia condição
JNZ LABEL_THEN, TEMP1 # Salta para then se verdadeiro
MOV C, B              # Bloco else (condição falsa)
JMP LABEL_FIM         # Pula o then
LBL LABEL_THEN        # Início do then
MOV C, A              # Bloco then
LBL LABEL_FIM         # Fim do if
```

### 5. Repetição (WHILE)

**Regra**: `COM -> while EXP BLC`

```
# Código fonte
while A > B
begin
    A := A - 1
end

# Código intermediário
LBL LABEL_INI         # Início do while
GTR TEMP1, A, B       # Avalia condição
JNZ LABEL_BLOCO, TEMP1  # Salta se verdadeiro (entra no loop)
JMP LABEL_FIM         # Condição falsa, sai do loop
LBL LABEL_BLOCO       # Início do bloco
SUB TEMP2, A, 1       # Bloco do while
MOV A, TEMP2          # Atribuição
JMP LABEL_INI         # Volta para o início
LBL LABEL_FIM         # Fim do while
```

### 6. Leitura e Escrita

**READ**:
```
# Código fonte
read(X)

# Código intermediário
READ X
```

**WRITE**:
```
# Código fonte
write(X + Y)

# Código intermediário
ADD TEMP1, X, Y
WRITE TEMP1
```

### 7. Chamada de Função

```
# Código fonte
resultado := soma(10, 20)

# Código intermediário
PUSH 10              # Empilha primeiro argumento
PUSH 20              # Empilha segundo argumento
CALL soma            # Chama função
POP TEMP1            # Desempilha resultado
MOV resultado, TEMP1 # Atribui resultado
```

## Exemplo Completo

### Código Fonte
```pascal
program exemplo;
var
    a, b, c : integer;
begin
    a := 10;
    b := 20;
    while a > b
    begin
        c := a + b;
        a := a - 1;
    end
end
```

### Código Intermediário Gerado
```
MOV a, 10
MOV b, 20
LBL LABEL1
GTR TEMP1, a, b
JMZ LABEL2, TEMP1
ADD TEMP2, a, b
MOV c, TEMP2
SUB TEMP3, a, 1
MOV a, TEMP3
JMP LABEL1
LBL LABEL2
```

## Algoritmo de Geração

```python
def gerar_codigo(no):
    """
    Percorre a árvore em pós-ordem gerando código
    """
    # Processar filhos primeiro
    for filho in no.filhos:
        codigo_filho = gerar_codigo(filho)
    
    # Gerar código para este nó
    codigo_no = formatar_instrucoes(no, codigo_filhos)
    
    return codigo_no
```

### Passos

1. **Percorrer árvore em pós-ordem** (filhos antes do pai)
2. **Identificar padrão** da regra sintática do nó
3. **Gerar instruções** conforme o padrão
4. **Inserir código dos filhos** nas posições apropriadas
5. **Criar variáveis temporárias** conforme necessário
6. **Criar labels** para controle de fluxo

## Formato de Saída

O código intermediário será apresentado em formato legível:

```
   1: MOV a, 10
   2: MOV b, 20
   3: LBL LABEL1
   4: GTR TEMP1, a, b
   5: JMZ LABEL2, TEMP1
   6: ADD TEMP2, a, b
   7: MOV c, TEMP2
   8: SUB TEMP3, a, 1
   9: MOV a, TEMP3
  10: JMP LABEL1
  11: LBL LABEL2
```

## Observações

- **Sem otimização** nesta fase - código pode ter redundâncias
- **Independente de máquina** - facilita portabilidade
- **Base para otimizações** posteriores
- **Facilita geração** de código de máquina final
