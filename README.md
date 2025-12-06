# Compilador Pascal Simplificado

Compilador para uma versão simplificada da linguagem Pascal, desenvolvido como trabalho da disciplina de Compiladores.

## Estrutura do Projeto

```
compiler/
├── src/
│   ├── lexer.py          # Analisador léxico (implementado com PLY)
│   └── parser.py         # Analisador sintático (implementado com PLY)
├── examples/
│   ├── teste_simples.sp     # Exemplo simples
│   ├── exemplo_circulo.sp   # Exemplo completo com funções
│   ├── erro_pontovirgula.sp # Exemplo com erros de ponto-e-vírgula
│   ├── erro_estrutura.sp    # Exemplo com erros de estrutura
│   └── erro_if.sp           # Exemplo com erros em if
├── slides/                  # Slides do professor
├── gramatica.md             # Gramática sem ambiguidades
├── first_follow.md          # Conjuntos First e Follow
├── main.py                  # Script principal
└── README.md                # Este arquivo
```

## Instalação

1. **Clone o repositório** (se aplicável)

2. **Crie e ative o ambiente virtual**:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

3. **Instale as dependências**:
```bash
pip install ply
```

## Uso

### Analisar um arquivo .sp

```bash
python main.py [opções] <arquivo.sp>
```

**Opções:**
- `-l, --lexico`: Apenas análise léxica
- `-s, --sintatico`: Apenas análise sintática  
- `-c, --completo`: Análise léxica e sintática (padrão)

### Exemplos:

```bash
# Análise completa (léxica + sintática)
python main.py examples/teste_simples.sp

# Apenas análise léxica
python main.py -l examples/teste_simples.sp

# Apenas análise sintática
python main.py -s examples/exemplo_circulo.sp

# Exemplo completo
python main.py examples/exemplo_circulo.sp
```

## Analisador Léxico

O analisador léxico foi implementado usando **PLY (Python Lex-Yacc)** e reconhece os seguintes tokens:

### Palavras Reservadas
- `program`, `begin`, `end`
- `const`, `type`, `var`, `function`
- `while`, `if`, `then`, `else`
- `write`, `read`
- `integer`, `real`, `array`, `of`, `record`

### Identificadores e Literais
- **ID**: Identificadores (começam com letra, podem conter letras, dígitos e `_`)
- **NUMBER**: Números inteiros ou reais (podem ter no máximo um ponto decimal)
- **STRING**: Strings entre aspas duplas

### Operadores
- **Matemáticos**: `+`, `-`, `*`, `/`
- **Relacionais**: `>`, `<`, `=`, `!`

### Símbolos Especiais
- `:=` (atribuição)
- `;` (ponto e vírgula)
- `:` (dois pontos)
- `,` (vírgula)
- `.` (ponto)
- `(` `)` (parênteses)
- `[` `]` (colchetes)

### Comentários
- Comentários são delimitados por `{ }` e são ignorados pelo analisador

## Analisador Sintático

O analisador sintático foi implementado usando **PLY (Python Lex-Yacc) - módulo yacc** e realiza análise sintática LALR.

### Características

- **Tipo**: Parser LALR(1) gerado automaticamente pelo PLY
- **Gramática**: Baseada na gramática LL(1) do Pascal Simplificado
- **Precedência**: Operadores têm precedência definida (*, / > +, - > comparações)
- **Tratamento de erros**: Modo pânico com mensagens descritivas
- **Saída**: Árvore sintática abstrata (AST) em formato de tuplas Python

### Estruturas Sintáticas Suportadas

- **Declarações**: Constantes, tipos customizados, variáveis
- **Funções**: Com parâmetros e variáveis locais
- **Comandos**:
  - Atribuição simples e com acesso a arrays/records
  - Laços `while`
  - Condicionais `if-then-else`
  - Entrada/saída `read` e `write`
- **Expressões**:
  - Aritméticas com precedência correta
  - Comparações (relacionais)
  - Chamadas de função
  - Acesso a arrays e campos de records

### Detecção de Erros

O analisador sintático detecta e reporta:
- Tokens inesperados
- Ausência de tokens obrigatórios (`;`, `end`, etc.)
- Estruturas sintáticas incorretas
- Fim de arquivo inesperado

Após encontrar um erro, o parser tenta continuar a análise (modo pânico) para detectar múltiplos erros em uma única execução.

## Formato dos Arquivos .sp

Os programas em Pascal Simplificado devem ter a extensão `.sp` e seguir a gramática definida em `gramatica.md`.

### Exemplo Mínimo:

```pascal
program exemplo;
var
    x : integer;
begin
    x := 10;
    write("Valor de x: ");
    write(x);
end
```

## Características da Gramática

- Gramática **LL(1)** (sem ambiguidades)
- Suporta:
  - Declaração de constantes, tipos e variáveis
  - Definição de funções com parâmetros
  - Tipos primitivos (integer, real)
  - Arrays e Records
  - Comandos de atribuição, laços (while) e condicionais (if-then-else)
  - Entrada/saída (read/write)
  - Expressões matemáticas e lógicas
  - Acesso a campos de records e elementos de arrays

## Próximos Passos

- [x] Implementar analisador léxico
- [x] Implementar analisador sintático
- [ ] Implementar analisador semântico
- [ ] Implementar geração de código intermediário
- [ ] Implementar otimizações
- [ ] Implementar geração de código de máquina

## Testes

Para testar o analisador léxico, execute:

```bash
# Teste básico (interno ao lexer.py)
python src/lexer.py

# Testes com exemplos
python main.py examples/teste_simples.sp
python main.py examples/exemplo_circulo.sp
```

## Saída Esperada

O analisador léxico gera uma tabela com:
- **Token**: Tipo do token reconhecido
- **Lexema**: Sequência de caracteres que forma o token
- **Linha**: Número da linha onde o token foi encontrado

Exemplo:
```
Token                Lexema               Linha     
--------------------------------------------------
PROGRAM              program              3         
ID                   teste_simples        3         
SEMICOLON            ;                    3         
...
```

## Tratamento de Erros

O analisador léxico reporta caracteres ilegais indicando:
- O caractere não reconhecido
- A linha onde o erro ocorreu

## Autor

Desenvolvido como trabalho acadêmico da disciplina de Compiladores.

## Licença

Este projeto é de uso acadêmico.
