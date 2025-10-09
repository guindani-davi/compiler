import ply.lex as lex

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

tokens = [
    "ID",
    "NUM_INT",
    "NUM_REAL",
    "STRING",
    "ASSIGN",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "EQUALS",
    "DIFF",
    "LT",
    "LE",
    "GT",
    "GE",
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "SEMICOLON",
    "COLON",
    "COMMA",
    "DOT",
    "ERROR",
] + list(reserved.values())

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


def t_ASSIGN(t):
    r":="
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


def t_NUM_REAL(t):
    r"[0-9]+\.[0-9]+"
    t.value = float(t.value)
    return t


def t_NUM_INT(t):
    r"0|[1-9][0-9]*"
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'"([^"\n]|"")*"'
    t.value = t.value[1:-1].replace('""', '"')
    return t


def t_ID(t):
    r"[A-Za-z][A-Za-z0-9_]*"
    t.type = reserved.get(t.value.lower(), "ID")
    return t


def t_COMMENT_LINE(t):
    r"//[^\n]*"
    pass


def t_COMMENT_BLOCK1(t):
    r"\{[^}]*\}"
    t.lexer.lineno += t.value.count("\n")
    pass


def t_COMMENT_BLOCK2(t):
    r"\(\*(.|\n)*?\*\)"
    t.lexer.lineno += t.value.count("\n")
    pass


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


t_ignore = " \t\r"

errors_list = []


def t_error(t):
    error_token = lex.LexToken()
    error_token.type = "ERROR"
    error_token.value = t.value[0]
    error_token.lineno = t.lexer.lineno
    error_token.lexpos = t.lexpos

    errors_list.append(error_token)

    print(f"ERRO LÉXICO: Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")

    t.lexer.skip(1)

    return error_token


lexer = lex.lex()


def test_lexer(data):
    global errors_list
    errors_list = []

    lexer.input(data)
    tokens_list = []

    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append(tok)

        if tok.type == "ERROR":
            print(f"Linha {tok.lineno}: {'>>> ERROR <<<':15} = '{tok.value}'")
        else:
            print(f"Linha {tok.lineno}: {tok.type:15} = {tok.value}")

    return tokens_list


def analyze_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = f.read()

        print(f"Analisando arquivo: {filename}")
        print("=" * 60)

        tokens_list = test_lexer(data)

        print("=" * 60)
        print(f"Total de tokens encontrados: {len(tokens_list)}")

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
    import sys

    if len(sys.argv) > 1:
        analyze_file(sys.argv[1])
    else:
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
