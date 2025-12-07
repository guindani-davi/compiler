# Otimização de Código

## Objetivo

Melhorar as características do código intermediário sem alterar seu comportamento, reduzindo o número de instruções e melhorando a eficiência.

### Princípios

- **Não altera o funcionamento**: O programa otimizado deve produzir os mesmos resultados
- **Não altera a complexidade**: Otimizações alteram constantes multiplicativas, não a ordem do algoritmo
- **Identifica oportunidades**: Remove redundâncias e código desnecessário

## Otimização Implementada: Eliminação de Código Morto

### Conceito

**Código morto** é qualquer instrução que não afeta o resultado final do programa. Existem três tipos principais:

1. **Código inalcançável**: Nunca será executado
2. **Código redundante**: Executa mas não tem efeito
3. **Variáveis não utilizadas**: Calculadas mas nunca lidas

### Técnica: Eliminação de Atribuições Não Utilizadas

Remove instruções que atribuem valores a variáveis que nunca são lidas posteriormente.

#### Algoritmo

1. **Análise de uso**: Percorrer código identificando quais variáveis são **lidas**
2. **Marcar necessárias**: Marcar instruções que:
   - Produzem valores lidos
   - Têm efeitos colaterais (WRITE, CALL, READ)
   - Controlam fluxo (JMP, JNZ, LBL)
3. **Remover desnecessárias**: Eliminar instruções não marcadas

#### Exemplo 1: Variável Temporária Não Usada

**Antes da otimização:**
```
1: MOV TEMP1, 10          # TEMP1 calculado mas nunca usado
2: MOV TEMP2, 20
3: ADD TEMP3, TEMP2, 5
4: MOV resultado, TEMP3
5: WRITE resultado
```

**Depois da otimização:**
```
1: MOV TEMP2, 20
2: ADD TEMP3, TEMP2, 5
3: MOV resultado, TEMP3
4: WRITE resultado
```

**Removido**: Linha 1 (TEMP1 nunca é lido)

#### Exemplo 2: Atribuição Sobrescrita

**Antes da otimização:**
```
1: MOV x, 10              # x sobrescrito antes de ser usado
2: MOV x, 20
3: WRITE x
```

**Depois da otimização:**
```
1: MOV x, 20
2: WRITE x
```

**Removido**: Linha 1 (x é sobrescrito na linha 2 antes de ser lido)

#### Exemplo 3: Resultado de Expressão Não Utilizado

**Antes da otimização:**
```
1: ADD TEMP1, a, b        # Cálculo feito mas resultado não usado
2: MOV TEMP2, 5
3: MUL TEMP3, TEMP2, 2
4: MOV x, TEMP3
5: WRITE x
```

**Depois da otimização:**
```
1: MOV TEMP2, 5
2: MUL TEMP3, TEMP2, 2
3: MOV x, TEMP3
4: WRITE x
```

**Removido**: Linha 1 (TEMP1 nunca é usado)

### Instruções Preservadas

Mesmo que não sejam lidas, as seguintes instruções **nunca** são removidas:

- **WRITE**: Produz saída (efeito colateral)
- **READ**: Lê entrada (efeito colateral)
- **CALL**: Chama função (pode ter efeitos colaterais)
- **RET**: Retorna de função (controle de fluxo)
- **JMP, JNZ**: Saltos (controle de fluxo)
- **LBL**: Labels (destino de saltos)
- **PUSH, POP**: Manipulação de pilha (necessárias para funções)

### Limitações

Esta otimização é **local** e não considera:
- Fluxo de controle entre blocos básicos
- Uso de variáveis em funções chamadas
- Aliases (mesma variável com nomes diferentes)

### Benefícios

- **Reduz tamanho do código**: Menos instruções
- **Melhora legibilidade**: Remove poluição visual
- **Pode melhorar desempenho**: Menos instruções para executar
- **Simplifica**: Remove cálculos desnecessários

## Exemplo Completo

### Código Fonte
```pascal
program teste;
var
    a, b, c, x : integer;
begin
    a := 10;        { usado }
    b := 20;        { não usado }
    c := a + 5;     { não usado }
    x := a * 2;     { usado }
    write(x)
end
```

### Código Intermediário SEM Otimização
```
1: MOV TEMP1, 10
2: MOV a, TEMP1
3: MOV TEMP2, 20
4: MOV b, TEMP2          # Linha morta: b nunca usado
5: MOV TEMP3, 5
6: ADD TEMP4, a, TEMP3
7: MOV c, TEMP4          # Linha morta: c nunca usado
8: MOV TEMP5, 2
9: MUL TEMP6, a, TEMP5
10: MOV x, TEMP6
11: WRITE x
```

### Código Intermediário COM Otimização
```
1: MOV TEMP1, 10
2: MOV a, TEMP1
3: MOV TEMP5, 2
4: MUL TEMP6, a, TEMP5
5: MOV x, TEMP6
6: WRITE x
```

**Linhas removidas**: 3, 4, 5, 6, 7 (5 instruções eliminadas, redução de 45%)

## Como Usar

```bash
# Ver código intermediário SEM otimização
uv run main.py -ci examples/teste.sp

# Ver código intermediário COM otimização
uv run main.py -opt examples/teste.sp

# Ver análise completa COM otimização
uv run main.py -c examples/teste.sp
```

## Estatísticas

O otimizador fornece estatísticas sobre:
- Total de instruções originais
- Total de instruções após otimização
- Número de instruções removidas
- Percentual de redução
