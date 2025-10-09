"""
Analisador Sintático para a linguagem SimplePascal
Implementado usando PLY (Python Lex-Yacc)
"""

import ply.yacc as yacc
from lexer import tokens, lexer

# Regras da gramática principal


def p_programa(p):
    """PROGRAMA : PROGRAM ID SEMICOLON CORPO"""
    p[0] = ("programa", p[2], p[4])


def p_corpo(p):
    """CORPO : DECLARACOES BEGIN LISTA_COM END
    | BEGIN LISTA_COM END"""
    if len(p) == 5:
        p[0] = ("corpo", p[1], p[3])
    else:
        p[0] = ("corpo", None, p[2])


def p_declaracoes(p):
    """DECLARACOES : DEF_CONST DEF_TIPOS DEF_VAR LISTA_FUNC
    | empty"""
    if len(p) == 5:
        p[0] = ("declaracoes", p[1], p[2], p[3], p[4])
    else:
        p[0] = ("declaracoes", None)


def p_def_const(p):
    """DEF_CONST : CONST LISTA_CONST
    | empty"""
    if len(p) == 3:
        p[0] = ("def_const", p[2])
    else:
        p[0] = None


def p_lista_const(p):
    """LISTA_CONST : CONSTANTE LISTA_CONST
    | CONSTANTE"""
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]


def p_constante(p):
    """CONSTANTE : ID ASSIGN CONST_VALOR SEMICOLON"""
    p[0] = ("constante", p[1], p[3])


def p_const_valor(p):
    """CONST_VALOR : STRING
    | EXP_MAT"""
    p[0] = p[1]


def p_def_tipos(p):
    """DEF_TIPOS : TYPE LISTA_TIPOS
    | empty"""
    if len(p) == 3:
        p[0] = ("def_tipos", p[2])
    else:
        p[0] = None


def p_lista_tipos(p):
    """LISTA_TIPOS : TIPO SEMICOLON LISTA_TIPOS
    | TIPO"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_tipo(p):
    """TIPO : ID ASSIGN TIPO_DADO"""
    p[0] = ("tipo", p[1], p[3])


def p_tipo_dado(p):
    """TIPO_DADO : INTEGER
    | REAL
    | ARRAY LBRACKET NUM_INT RBRACKET OF TIPO_DADO
    | RECORD LISTA_VAR END
    | ID"""
    if len(p) == 2:
        p[0] = ("tipo_simples", p[1])
    elif p[1] == "array":
        p[0] = ("array", p[3], p[6])
    elif p[1] == "record":
        p[0] = ("record", p[2])
    else:
        p[0] = ("tipo_simples", p[1])


def p_def_var(p):
    """DEF_VAR : VAR LISTA_VAR
    | empty"""
    if len(p) == 3:
        p[0] = ("def_var", p[2])
    else:
        p[0] = None


def p_lista_var(p):
    """LISTA_VAR : VARIAVEL SEMICOLON LISTA_VAR
    | VARIAVEL"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_variavel(p):
    """VARIAVEL : LISTA_ID COLON TIPO_DADO"""
    p[0] = ("variavel", p[1], p[3])


def p_lista_id(p):
    """LISTA_ID : ID COMMA LISTA_ID
    | ID"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_lista_func(p):
    """LISTA_FUNC : FUNCAO LISTA_FUNC
    | empty"""
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_funcao(p):
    """FUNCAO : FUNCTION ID LPAREN PARAM_FORM RPAREN COLON TIPO_DADO BLOCO_FUNCAO
    | FUNCTION ID LPAREN RPAREN COLON TIPO_DADO BLOCO_FUNCAO"""
    if len(p) == 9:
        p[0] = ("funcao", p[2], p[4], p[7], p[8])
    else:
        p[0] = ("funcao", p[2], None, p[6], p[7])


def p_param_form(p):
    """PARAM_FORM : PARAM COMMA PARAM_FORM
    | PARAM"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_param(p):
    """PARAM : LISTA_ID COLON TIPO_DADO"""
    p[0] = ("param", p[1], p[3])


def p_bloco_funcao(p):
    """BLOCO_FUNCAO : DEF_VAR BLOCO
    | BLOCO"""
    if len(p) == 3:
        p[0] = ("bloco_funcao", p[1], p[2])
    else:
        p[0] = ("bloco_funcao", None, p[1])


def p_bloco(p):
    """BLOCO : BEGIN LISTA_COM END
    | COMANDO"""
    if len(p) == 4:
        p[0] = ("bloco", p[2])
    else:
        p[0] = ("bloco", [p[1]])


def p_lista_com(p):
    """LISTA_COM : COMANDO SEMICOLON LISTA_COM
    | COMANDO"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_comando(p):
    """COMANDO : NOME ASSIGN VALOR
    | WHILE EXP_LOGICA BLOCO
    | IF EXP_LOGICA THEN BLOCO ELSE BLOCO
    | IF EXP_LOGICA THEN BLOCO
    | WRITE LPAREN EXP_MAT RPAREN
    | WRITE LPAREN STRING RPAREN
    | READ LPAREN NOME RPAREN
    | BEGIN LISTA_COM END"""
    if len(p) == 4 and p[2] == ":=":
        p[0] = ("atribuicao", p[1], p[3])
    elif p[1] == "while":
        p[0] = ("while", p[2], p[3])
    elif p[1] == "if" and len(p) == 7:
        p[0] = ("if_else", p[2], p[4], p[6])
    elif p[1] == "if" and len(p) == 5:
        p[0] = ("if", p[2], p[4])
    elif p[1] == "write":
        p[0] = ("write", p[3])
    elif p[1] == "read":
        p[0] = ("read", p[3])
    else:  # BEGIN LISTA_COM END
        p[0] = ("bloco", p[2])


def p_valor(p):
    """VALOR : EXP_MAT
    | ID LISTA_ARG"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ("call", p[1], p[2])


def p_lista_arg(p):
    """LISTA_ARG : LPAREN LISTA_EXP RPAREN
    | LPAREN RPAREN
    | empty"""
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 3:
        p[0] = []
    else:
        p[0] = None


def p_lista_exp(p):
    """LISTA_EXP : EXP_MAT COMMA LISTA_EXP
    | EXP_MAT"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_exp_logica(p):
    """EXP_LOGICA : EXP_REL"""
    p[0] = p[1]


def p_exp_rel(p):
    """EXP_REL : EXP_MAT OP_REL EXP_MAT
    | EXP_MAT"""
    if len(p) == 4:
        p[0] = ("exp_rel", p[1], p[2], p[3])
    else:
        p[0] = p[1]


def p_op_rel(p):
    """OP_REL : EQUALS
    | DIFF
    | LT
    | LE
    | GT
    | GE"""
    p[0] = p[1]


def p_exp_mat(p):
    """EXP_MAT : TERMO PLUS EXP_MAT
    | TERMO MINUS EXP_MAT
    | TERMO
    """
    if len(p) == 4:
        p[0] = ("exp_mat", p[1], p[2], p[3])
    else:
        p[0] = p[1]


def p_termo(p):
    """TERMO : FATOR TIMES TERMO
    | FATOR DIVIDE TERMO
    | FATOR"""
    if len(p) == 4:
        p[0] = ("termo", p[1], p[2], p[3])
    else:
        p[0] = p[1]


def p_fator(p):
    """FATOR : PARAMETRO
    | LPAREN EXP_MAT RPAREN"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_parametro(p):
    """PARAMETRO : NOME
    | NUM_INT
    | NUM_REAL"""
    p[0] = p[1]


def p_nome(p):
    """NOME : ID NOME_CONT
    | ID"""
    if len(p) == 3:
        p[0] = ("nome", p[1], p[2])
    else:
        p[0] = p[1]


def p_nome_cont(p):
    """NOME_CONT : DOT ID NOME_CONT
    | LBRACKET EXP_MAT RBRACKET NOME_CONT
    | empty"""
    if len(p) == 4 and p[1] == ".":
        p[0] = [("field", p[2])] + (p[3] if p[3] else [])
    elif len(p) == 5 and p[1] == "[":
        p[0] = [("index", p[2])] + (p[4] if p[4] else [])
    else:
        p[0] = None


def p_empty(p):
    "empty :"
    pass


def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo a '{p.value}' na linha {p.lineno}.")
    else:
        print("Erro de sintaxe: fim de arquivo inesperado.")


parser = yacc.yacc()


def parse_file(filename):
    """Analisa um arquivo fonte SimplePascal"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = f.read()

        print(f"Analisando arquivo: {filename}")
        print("=" * 60)

        # Reseta o lexer
        lexer.lineno = 1

        # Faz o parsing
        result = parser.parse(data, lexer=lexer)

        print("=" * 60)
        if result:
            print("✅ Análise sintática concluída com sucesso!")
            return result
        else:
            print("❌ Análise sintática falhou!")
            return None

    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado!")
        return None
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")
        return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python parser.py <arquivo-fonte>")
        sys.exit(1)

    result = parse_file(sys.argv[1])
    if result:
        print("\nÁrvore Sintática:")
        import pprint

        pprint.pprint(result, width=100)
