# Análise Semântica

## Objetivo
Percorrer a Árvore Sintática para validar regras semânticas que avaliam a relação entre tokens distantes entre si, utilizando informações armazenadas na Tabela de Símbolos.

## Tabela de Símbolos

### Estrutura
Estrutura de dados contendo um registro para cada identificador usado no programa. Cada registro contém:

- **Nome**: Identificador único
- **Classificação**: variável, constante, função, parâmetro, tipo
- **Tipo**: inteiro, real, booleano, caractere, array, registro, void
- **Escopo**: Global, nome da função/procedimento
- **Quantidade de parâmetros**: Para funções/procedimentos
- **Ordem**: Para parâmetros (1º, 2º, 3º...)

### Exemplo
```pascal
procedure Fatorial(x: inteiro): inteiro
inicio
    se x > 1 entao
        retorne x * fatorial(x-1);
    retorne 1;
fim;
```

| Nome     | Classificação | Tipo    | Escopo   | Qtd Params | Ordem |
|----------|---------------|---------|----------|------------|-------|
| Fatorial | função        | inteiro | Global   | 1          | -     |
| x        | parâmetro     | inteiro | Fatorial | -          | 1º    |

## Regras Semânticas

### 1. Declaração de Identificadores
- **Regra**: Todo identificador deve ser declarado antes de ser utilizado
- **Validação**: Consultar tabela de símbolos antes de usar qualquer identificador
- **Erro**: "Identificador '{nome}' não declarado"

### 2. Uso de Variáveis
- **Regra**: Somente identificadores do tipo variável podem aparecer do lado esquerdo de uma atribuição
- **Validação**: Verificar classificação do identificador
- **Erro**: "'{nome}' não pode ser usado em atribuição (não é variável)"

### 3. Compatibilidade de Tipos em Atribuições
- **Regra**: O tipo da expressão do lado direito deve ser compatível com o tipo da variável do lado esquerdo
- **Validação**: Verificar tipos e permitir conversões implícitas quando aplicável
- **Conversões permitidas**:
  - inteiro → real (implícita)
  - inteiro → inteiro (exata)
  - real → real (exata)
  - booleano → booleano (exata)
  - caractere → caractere (exata)
- **Erro**: "Tipos incompatíveis: não é possível atribuir {tipo_expr} a {tipo_var}"

### 4. Compatibilidade de Tipos em Expressões
- **Regra**: Operandos de operações aritméticas devem ser numéricos (inteiro ou real)
- **Regra**: Operandos de operações relacionais devem ser do mesmo tipo
- **Regra**: Operandos de operações lógicas devem ser booleanos
- **Tipo resultante**:
  - inteiro op inteiro → inteiro
  - real op inteiro → real
  - inteiro op real → real
  - real op real → real
  - qualquer op_relacional qualquer → booleano
  - booleano op_logico booleano → booleano
- **Erro**: "Operação {op} inválida para tipos {tipo1} e {tipo2}"

### 5. Escopo de Identificadores
- **Regra**: Um identificador só pode ser usado dentro do escopo onde foi declarado
- **Escopo Global**: Visível em todo o programa
- **Escopo Local**: Visível apenas dentro da função/procedimento onde foi declarado
- **Precedência**: Identificadores locais têm precedência sobre globais com mesmo nome
- **Validação**: Verificar escopo atual ao usar identificador
- **Erro**: "Identificador '{nome}' fora do escopo"

### 6. Redeclaração de Identificadores
- **Regra**: Um identificador não pode ser redeclarado no mesmo escopo
- **Validação**: Verificar se já existe entrada na tabela para o escopo atual
- **Erro**: "Identificador '{nome}' já declarado no escopo {escopo}"

### 7. Chamadas de Função
- **Regra**: Quantidade de argumentos deve ser igual à quantidade de parâmetros
- **Regra**: Tipo de cada argumento deve ser compatível com o tipo do parâmetro correspondente
- **Validação**: 
  - Verificar se identificador é uma função
  - Comparar quantidade de argumentos
  - Comparar tipos na ordem correta
- **Erro**: 
  - "Função '{nome}' espera {n} argumentos, mas recebeu {m}"
  - "Argumento {i} incompatível: esperado {tipo_param}, recebido {tipo_arg}"

### 8. Uso de Funções
- **Regra**: Funções com retorno devem ser usadas em expressões ou atribuições
- **Regra**: Procedimentos (sem retorno/void) devem ser usados como comandos
- **Validação**: Verificar tipo de retorno
- **Erro**: "Procedimento '{nome}' não pode ser usado em expressão"

### 9. Comandos de Controle
- **Regra**: Condições em SE-ENTAO-SENAO e ENQUANTO devem ser booleanas
- **Validação**: Verificar tipo da expressão condicional
- **Erro**: "Condição deve ser booleana, mas é {tipo}"

### 10. Comando RETORNE
- **Regra**: Comando RETORNE só pode ser usado dentro de funções
- **Regra**: Tipo da expressão retornada deve ser compatível com tipo de retorno da função
- **Validação**: 
  - Verificar se está dentro de função
  - Comparar tipo da expressão com tipo da função
- **Erro**: 
  - "RETORNE fora de função"
  - "Tipo de retorno incompatível: esperado {tipo_funcao}, mas retorna {tipo_expr}"

### 11. Arrays
- **Regra**: Índices de arrays devem ser inteiros
- **Regra**: Dimensões devem corresponder à declaração
- **Validação**: Verificar tipo dos índices
- **Erro**: 
  - "Índice de array deve ser inteiro, mas é {tipo}"
  - "Array '{nome}' requer {n} índices, mas recebeu {m}"

### 12. Registros
- **Regra**: Campos acessados devem existir no registro
- **Regra**: Identificador deve ser do tipo registro
- **Validação**: Verificar se campo existe na definição do tipo
- **Erro**: 
  - "'{nome}' não é um registro"
  - "Campo '{campo}' não existe no registro '{tipo}'"

## Algoritmo de Análise Semântica

### Estrutura Geral
```python
def analisar_semantica(no):
    """
    Percorre a árvore sintática validando regras semânticas
    """
    # Processar filhos primeiro (bottom-up)
    for filho in no.filhos:
        analisar_semantica(filho)
    
    # Atualizar tabela de símbolos se necessário
    atualizar_tabela_simbolos(no)
    
    # Validar regras semânticas para este nó
    validar_regras(no)
```

### Atualização da Tabela de Símbolos
```python
def atualizar_tabela_simbolos(no):
    """
    Atualiza tabela em sub-árvores de declaração
    """
    if esta_em_declaracao(no):
        if no.tipo == 'ID':
            # Adicionar nova entrada
            adicionar_identificador(no)
        else:
            # Atualizar entrada existente com mais informações
            atualizar_identificador(no)
```

### Validação de Regras
```python
def validar_regras(no):
    """
    Valida regras semânticas baseado no tipo do nó
    """
    if no.tipo == 'atribuicao':
        validar_atribuicao(no)
    elif no.tipo == 'chamada_funcao':
        validar_chamada_funcao(no)
    elif no.tipo == 'expressao':
        validar_expressao(no)
    elif no.tipo == 'se' or no.tipo == 'enquanto':
        validar_condicao(no)
    elif no.tipo == 'retorne':
        validar_retorne(no)
    # ... outras validações
```

## Implementação

### Estrutura de Arquivos
- `src/symbol_table.py`: Implementação da tabela de símbolos
- `src/semantic.py`: Analisador semântico com validação de regras
- `src/semantic_types.py`: Definições de tipos e regras de compatibilidade

### Integração com Parser
O parser deve gerar uma AST que será percorrida pelo analisador semântico. Informações sobre tipos e declarações são coletadas durante a travessia.

### Tratamento de Erros
- Coletar todos os erros semânticos encontrados
- Reportar linha e tipo do erro
- Continuar análise para encontrar múltiplos erros quando possível
- Não gerar código se houver erros semânticos
