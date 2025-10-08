"""
Analisador Léxico para a linguagem SimplePascal
Implementado usando PLY (Python Lex-Yacc)
"""

import ply.lex as lex

# Palavras reservadas
reserved = {
    "program": "PROGRAM",
    "const": "CONST",
    "type": "TYPE",
    "var": "VAR",
    "begin": "BEGIN",
    "end": "END",
    "function": "FUNCTION",
    "of": "OF",
    "record": "RECORD",
    "array": "ARRAY",
    "integer": "INTEGER",
    "real": "REAL",
    "while": "WHILE",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "write": "WRITE",
    "read": "READ",
}

# Lista de tokens
tokens = [
    "ID",  # Identificadores
    "NUM_INT",  # Números inteiros
    "NUM_REAL",  # Números reais
    "STRING",  # Strings
    # Operadores
    "ASSIGN",  # :=
    "PLUS",  # +
    "MINUS",  # -
    "TIMES",  # *
    "DIVIDE",  # /
    "EQUALS",  # =
    "DIFF",  # <>
    "LT",  # <
    "LE",  # <=
    "GT",  # >
    "GE",  # >=
    # Delimitadores
    "LPAREN",  # (
    "RPAREN",  # )
    "LBRACKET",  # [
    "RBRACKET",  # ]
    "SEMICOLON",  # ;
    "COLON",  # :
    "COMMA",  # ,
    "DOT",  # .
    "DOTDOT",  # ..
    # Erros
    "ERROR",  # Token de erro léxico
] + list(reserved.values())

# Regras de expressões regulares para tokens simples
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_SEMICOLON = r";"
t_COMMA = r","


# Regras para tokens que precisam de precedência
def t_ASSIGN(t):
    r":="
    return t


def t_DOTDOT(t):
    r"\.\."
    return t


def t_DOT(t):
    r"\."
    return t


def t_COLON(t):
    r":"
    return t


def t_LE(t):
    r"<="
    return t


def t_GE(t):
    r">="
    return t


def t_DIFF(t):
    r"<>"
    return t


def t_LT(t):
    r"<"
    return t


def t_GT(t):
    r">"
    return t


def t_EQUALS(t):
    r"="
    return t


# Números reais (deve vir antes de inteiros)
def t_NUM_REAL(t):
    r"[0-9]+\.[0-9]+"
    t.value = float(t.value)
    return t


# Números inteiros
def t_NUM_INT(t):
    r"0|[1-9][0-9]*"
    t.value = int(t.value)
    return t


# Strings
def t_STRING(t):
    r'"([^"\n]|"")*"'
    # Remove aspas e trata aspas duplas escapadas
    t.value = t.value[1:-1].replace('""', '"')
    return t


# Identificadores e palavras reservadas
def t_ID(t):
    r"[A-Za-z][A-Za-z0-9_]*"
    t.type = reserved.get(t.value.lower(), "ID")  # Verifica se é palavra reservada
    return t


# Comentário de linha //
def t_COMMENT_LINE(t):
    r"//[^\n]*"
    pass  # Ignora comentários


# Comentário de bloco { }
def t_COMMENT_BLOCK1(t):
    r"\{[^}]*\}"
    # Conta linhas dentro do comentário
    t.lexer.lineno += t.value.count("\n")
    pass  # Ignora comentários


# Comentário de bloco (* *)
def t_COMMENT_BLOCK2(t):
    r"\(\*(.|\n)*?\*\)"
    # Conta linhas dentro do comentário
    t.lexer.lineno += t.value.count("\n")
    pass  # Ignora comentários


# Conta linhas
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Ignora espaços e tabs
t_ignore = " \t\r"

# Lista para armazenar erros encontrados
errors_list = []


# Tratamento de erros
def t_error(t):
    """
    Trata erros léxicos criando um token ERROR.
    Não para a análise, continua processando o resto do arquivo.
    """
    # Cria token de erro com o caractere ilegal
    error_token = lex.LexToken()
    error_token.type = "ERROR"
    error_token.value = t.value[0]
    error_token.lineno = t.lexer.lineno
    error_token.lexpos = t.lexpos

    # Adiciona à lista de erros
    errors_list.append(error_token)

    # Imprime mensagem de erro mas continua análise
    print(f"ERRO LÉXICO: Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")

    # Pula o caractere ilegal e continua
    t.lexer.skip(1)

    # Retorna o token de erro
    return error_token


# Constrói o lexer
lexer = lex.lex()


# Função para testar o lexer
def test_lexer(data):
    """Função para testar o analisador léxico"""
    global errors_list
    errors_list = []  # Limpa lista de erros

    lexer.input(data)
    tokens_list = []

    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append(tok)

        # Marca tokens de erro com visual diferente
        if tok.type == "ERROR":
            print(f"Linha {tok.lineno}: {'>>> ERROR <<<':15} = '{tok.value}'")
        else:
            print(f"Linha {tok.lineno}: {tok.type:15} = {tok.value}")

    return tokens_list


# Função para ler arquivo fonte
def analyze_file(filename):
    """Analisa um arquivo fonte SimplePascal"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = f.read()

        print(f"Analisando arquivo: {filename}")
        print("=" * 60)

        tokens_list = test_lexer(data)

        print("=" * 60)
        print(f"Total de tokens encontrados: {len(tokens_list)}")

        # Conta erros
        num_errors = sum(1 for tok in tokens_list if tok.type == "ERROR")
        if num_errors > 0:
            print(f"ATENÇÃO: {num_errors} erro(s) léxico(s) encontrado(s)!")
        else:
            print("Análise léxica concluída sem erros!")

        return tokens_list

    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado!")
        return []
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")
        return []


if __name__ == "__main__":
    # Exemplo de uso
    import sys

    if len(sys.argv) > 1:
        # Se passou arquivo como argumento
        analyze_file(sys.argv[1])
    else:
        # Teste com código de exemplo
        test_code = """
        program exemplo;
        
        const
            PI := 3.14;
            MSG := "Hello, World!";
        
        var
            x, y: integer;
            z: real;
        
        begin
            x := 10;
            y := 20;
            z := x + y * 2.5;
            write("Resultado: ");
            write(z);
        end
        """

        print("Testando com código de exemplo:")
        print("=" * 60)
        test_lexer(test_code)
