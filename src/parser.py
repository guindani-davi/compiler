import ply.yacc as yacc
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from lexer import tokens, lexer

errors = []

start = "programa"


def p_programa(p):
    """programa : PROGRAM ID SEMICOLON corpo"""
    p[0] = ("PROGRAMA", p[2], p[4])
    print(f"Programa '{p[2]}' reconhecido com sucesso")


def p_corpo(p):
    """corpo : def_const def_tipos def_var lista_func BEGIN lista_comandos END"""
    p[0] = ("CORPO", p[1], p[2], p[3], p[4], p[6])


def p_def_const(p):
    """def_const : CONST lista_const
    |"""
    if len(p) == 3:
        p[0] = ("DEF_CONST", p[2])
    else:
        p[0] = None


def p_lista_const(p):
    """lista_const : constante lista_const
    | constante"""
    if len(p) == 3:
        p[0] = [p[1]] + (p[2] if isinstance(p[2], list) else [p[2]])
    else:
        p[0] = [p[1]]


def p_constante(p):
    """constante : ID ASSIGN const_valor SEMICOLON"""
    p[0] = ("CONSTANTE", p[1], p[3])


def p_const_valor(p):
    """const_valor : STRING
    | NUMBER"""
    p[0] = p[1]


def p_def_tipos(p):
    """def_tipos : TYPE lista_tipos
    |"""
    if len(p) == 3:
        p[0] = ("DEF_TIPOS", p[2])
    else:
        p[0] = None


def p_lista_tipos(p):
    """lista_tipos : tipo SEMICOLON lista_tipos
    | tipo SEMICOLON"""
    if len(p) == 4:
        p[0] = [p[1]] + (p[3] if isinstance(p[3], list) else [])
    else:
        p[0] = [p[1]]


def p_tipo(p):
    """tipo : ID ASSIGN tipo_dado"""
    p[0] = ("TIPO", p[1], p[3])


def p_tipo_dado(p):
    """tipo_dado : INTEGER
    | REAL
    | ARRAY LBRACKET NUMBER RBRACKET OF tipo_dado
    | RECORD lista_var END
    | ID"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ("RECORD", p[2])
    else:
        p[0] = ("ARRAY", p[3], p[6])


def p_def_var(p):
    """def_var : VAR lista_var
    |"""
    if len(p) == 3:
        p[0] = ("DEF_VAR", p[2])
    else:
        p[0] = None


def p_lista_var(p):
    """lista_var : variavel SEMICOLON lista_var
    | variavel SEMICOLON"""
    if len(p) == 4:
        p[0] = [p[1]] + (p[3] if isinstance(p[3], list) else [])
    else:
        p[0] = [p[1]]


def p_variavel(p):
    """variavel : lista_id COLON tipo_dado"""
    p[0] = ("VARIAVEL", p[1], p[3])


def p_lista_id(p):
    """lista_id : ID COMMA lista_id
    | ID"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_lista_func(p):
    """lista_func : funcao lista_func
    |"""
    if len(p) == 3:
        p[0] = [p[1]] + (p[2] if isinstance(p[2], list) else [])
    else:
        p[0] = []


def p_funcao(p):
    """funcao : FUNCTION ID LPAREN lista_param RPAREN COLON tipo_dado def_var BEGIN lista_comandos END"""
    p[0] = ("FUNCAO", p[2], p[4], p[7], p[8], p[10])


def p_lista_param(p):
    """lista_param : param_decl
    | param_decl SEMICOLON lista_param
    |"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2 and p[1]:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_param_decl(p):
    """param_decl : lista_id COLON tipo_dado"""
    p[0] = ("PARAMETRO", p[1], p[3])


def p_lista_comandos(p):
    """lista_comandos : comando SEMICOLON lista_comandos
    | comando
    |"""
    if len(p) == 4:
        p[0] = [p[1]] + (p[3] if isinstance(p[3], list) else [])
    elif len(p) == 2 and p[1]:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_comando_atrib(p):
    """comando : lvalue ASSIGN expressao"""
    p[0] = ("ATRIBUICAO", p[1], p[3])


def p_comando_while(p):
    """comando : WHILE expressao BEGIN lista_comandos END"""
    p[0] = ("WHILE", p[2], p[4])


def p_comando_if(p):
    """comando : IF expressao THEN BEGIN lista_comandos END else_parte"""
    p[0] = ("IF", p[2], p[5], p[7])


def p_comando_write_string(p):
    """comando : WRITE LPAREN STRING RPAREN"""
    p[0] = ("WRITE", p[3])


def p_comando_write_expr(p):
    """comando : WRITE LPAREN expressao RPAREN"""
    p[0] = ("WRITE", p[3])


def p_comando_read(p):
    """comando : READ LPAREN ID RPAREN"""
    p[0] = ("READ", p[3])


def p_else_parte(p):
    """else_parte : ELSE BEGIN lista_comandos END
    |"""
    if len(p) == 5:
        p[0] = ("ELSE", p[3])
    else:
        p[0] = None


def p_lvalue_id(p):
    """lvalue : ID"""
    p[0] = p[1]


def p_lvalue_array(p):
    """lvalue : ID LBRACKET expressao RBRACKET"""
    p[0] = ("ARRAY_ACCESS", p[1], p[3])


def p_lvalue_field(p):
    """lvalue : ID DOT ID"""
    p[0] = ("FIELD_ACCESS", p[1], p[3])


def p_lvalue_array_field(p):
    """lvalue : ID LBRACKET expressao RBRACKET DOT ID"""
    p[0] = ("FIELD_ACCESS", ("ARRAY_ACCESS", p[1], p[3]), p[6])


def p_expressao_comp(p):
    """expressao : expressao op_comp expressao"""
    p[0] = ("OP_COMP", p[2], p[1], p[3])


def p_expressao_arit(p):
    """expressao : expressao op_arit expressao"""
    p[0] = ("OP_ARIT", p[2], p[1], p[3])


def p_expressao_prim(p):
    """expressao : primario"""
    p[0] = p[1]


def p_primario_numero(p):
    """primario : NUMBER"""
    p[0] = p[1]


def p_primario_id(p):
    """primario : ID"""
    p[0] = p[1]


def p_primario_array(p):
    """primario : ID LBRACKET expressao RBRACKET"""
    p[0] = ("ARRAY_ACCESS", p[1], p[3])


def p_primario_field(p):
    """primario : ID DOT ID"""
    p[0] = ("FIELD_ACCESS", p[1], p[3])


def p_primario_call(p):
    """primario : ID LPAREN lista_args RPAREN"""
    p[0] = ("CHAMADA_FUNCAO", p[1], p[3])


def p_lista_args(p):
    """lista_args : expressao COMMA lista_args
    | expressao
    |"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2 and p[1]:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_op_comp(p):
    """op_comp : GT
    | LT
    | EQUALS
    | EXCLAMATION"""
    p[0] = p[1]


def p_op_arit(p):
    """op_arit : PLUS
    | MINUS
    | TIMES
    | DIVIDE"""
    p[0] = p[1]


precedence = (
    ("left", "GT", "LT", "EQUALS", "EXCLAMATION"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
)


def p_error(p):
    global errors
    if p:
        error_msg = (
            f"Erro sintático na linha {p.lineno}: "
            f"Token inesperado '{p.value}' (tipo: {p.type})"
        )
        errors.append(error_msg)
        print(f"{error_msg}")

        parser.errok()
    else:
        error_msg = "Erro sintático: fim de arquivo inesperado"
        errors.append(error_msg)
        print(f"{error_msg}")


parser = yacc.yacc()


def parse(data, debug=False):
    global errors
    errors = []

    lexer.lineno = 1
    result = parser.parse(data, lexer=lexer, debug=debug)

    if errors:
        print(f"\n{len(errors)} erro(s) sintático(s) encontrado(s)")
        return None
    else:
        print("\nAnálise sintática concluída com sucesso!")
        return result


def parse_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = f.read()

        print(f"\n{'='*70}")
        print(f"Análise Sintática do arquivo: {filename}")
        print(f"{'='*70}\n")

        result = parse(data)

        print(f"\n{'='*70}")
        if result:
            print("Status: SUCESSO")
        else:
            print("Status: FALHA")
        print(f"{'='*70}\n")

        return result

    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado")
        return None
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")
        return None


if __name__ == "____":
    test_code = """
    program teste;
    var
        x : integer;
    begin
        x := 10
    end
    """

    print("=== Teste do Analisador Sintático ===\n")
    result = parse(test_code)
    if result:
        print("\nPrograma válido")
