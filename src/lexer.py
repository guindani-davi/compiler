"""
Analisador Léxico para Pascal Simplificado
Baseado na gramática sem ambiguidades definida em gramatica.md
Implementado usando PLY (Python Lex-Yacc)
"""

import ply.lex as lex

# Lista de tokens
tokens = (
    # Palavras reservadas
    "PROGRAM",
    "BEGIN",
    "END",
    "CONST",
    "TYPE",
    "VAR",
    "FUNCTION",
    "WHILE",
    "IF",
    "THEN",
    "ELSE",
    "WRITE",
    "READ",
    "INTEGER",
    "REAL",
    "ARRAY",
    "OF",
    "RECORD",
    # Identificadores e literais
    "ID",
    "NUMBER",
    "STRING",
    # Operadores matemáticos
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    # Operadores lógicos/relacionais
    "GT",  # >
    "LT",  # <
    "EQUALS",  # =
    "EXCLAMATION",  # !
    # Símbolos especiais
    "ASSIGN",  # :=
    "SEMICOLON",  # ;
    "COLON",  # :
    "COMMA",  # ,
    "DOT",  # .
    "LPAREN",  # (
    "RPAREN",  # )
    "LBRACKET",  # [
    "RBRACKET",  # ]
)

# Palavras reservadas (mapeamento para prioridade)
reserved = {
    "program": "PROGRAM",
    "begin": "BEGIN",
    "end": "END",
    "const": "CONST",
    "type": "TYPE",
    "var": "VAR",
    "function": "FUNCTION",
    "while": "WHILE",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "write": "WRITE",
    "read": "READ",
    "integer": "INTEGER",
    "real": "REAL",
    "array": "ARRAY",
    "of": "OF",
    "record": "RECORD",
}

# Expressões regulares simples para tokens
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_GT = r">"
t_LT = r"<"
t_EQUALS = r"="
t_EXCLAMATION = r"!"
t_ASSIGN = r":="
t_SEMICOLON = r";"
t_COLON = r":"
t_COMMA = r","
t_DOT = r"\."
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"

# Expressões regulares complexas (com funções)


def t_NUMBER(t):
    r"\d+\.?\d*|\d*\.\d+"
    """
    Números: sequência de dígitos podendo conter no máximo um ponto
    Exemplos: 123, 12.3, .789, 345.
    """
    if "." in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


def t_STRING(t):
    r'"[^"]*"'
    """
    Strings: sequência alfanumérica entre aspas duplas
    Remove as aspas do valor
    """
    t.value = t.value[1:-1]  # Remove as aspas
    return t


def t_ID(t):
    r"[a-zA-Z][a-zA-Z0-9_]*"
    """
    Identificadores: sequência alfanumérica iniciada por letra
    Pode conter underscores
    Verifica se é palavra reservada
    """
    t.type = reserved.get(t.value.lower(), "ID")  # Palavras reservadas têm prioridade
    return t


def t_COMMENT(t):
    r"\{[^}]*\}"
    """
    Comentários: texto entre chaves { }
    São ignorados pelo analisador léxico
    """
    pass  # Comentários são descartados


def t_newline(t):
    r"\n+"
    """
    Conta as quebras de linha para rastreamento de erros
    """
    t.lexer.lineno += len(t.value)


# Caracteres ignorados (espaços e tabs)
t_ignore = " \t"


def t_error(t):
    """
    Tratamento de erros léxicos
    Caracteres não reconhecidos são reportados
    """
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)


# Construir o analisador léxico
lexer = lex.lex()


# Função auxiliar para testar o lexer
def tokenize(data):
    """
    Tokeniza uma string de entrada e retorna lista de tokens
    """
    lexer.input(data)
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append(tok)
    return tokens_list


def print_tokens(data):
    """
    Imprime os tokens encontrados no formato legível
    """
    lexer.input(data)
    print(f"{'Token':<20} {'Lexema':<20} {'Linha':<10}")
    print("-" * 50)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"{tok.type:<20} {str(tok.value):<20} {tok.lineno:<10}")


if __name__ == "__main__":
    # Teste simples
    test_code = """
    program teste;
    const pi := 3.1415;
    var
        x, y : integer;
        z : real;
    begin
        x := 10;
        y := 20;
        z := x + y;
        write("Resultado");
    end
    """

    print("=== Teste do Analisador Léxico ===\n")
    print_tokens(test_code)
