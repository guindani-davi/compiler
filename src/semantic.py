from symbol_table import SymbolTable, Symbol


class SemanticError(Exception):
    def __init__(self, message, linha=None):
        self.message = message
        self.linha = linha
        super().__init__(self.format_message())

    def format_message(self):
        if self.linha:
            return f"Linha {self.linha}: {self.message}"
        return self.message


class SemanticAnalyzer:
    def __init__(self):
        self.tabela = SymbolTable()
        self.erros = []
        self.funcao_atual = None
        self.tipos_basicos = {"INTEGER", "REAL", "BOOLEAN", "CHAR", "STRING"}

    def analisar(self, ast):
        if ast is None:
            return False

        self.erros = []
        self.tabela.limpar()

        try:
            self.visitar(ast)
        except Exception as e:
            self.erros.append(f"Erro interno: {e}")

        return len(self.erros) == 0

    def adicionar_erro(self, mensagem, linha=None):
        if linha:
            self.erros.append(f"Linha {linha}: {mensagem}")
        else:
            self.erros.append(mensagem)

    def visitar(self, no):
        if no is None:
            return None

        if isinstance(no, tuple) and len(no) > 0:
            tipo_no = no[0]
            metodo = f"visitar_{tipo_no.lower()}"

            if hasattr(self, metodo):
                return getattr(self, metodo)(no)
            else:
                for filho in no[1:]:
                    self.visitar(filho)
                return None

        elif isinstance(no, list):
            for item in no:
                self.visitar(item)
            return None

        else:
            return no

    def visitar_programa(self, no):
        _, nome, corpo = no

        self.tabela.adicionar(nome, "programa", "void")

        self.visitar(corpo)

    def visitar_corpo(self, no):
        _, def_const, def_tipos, def_var, lista_func, lista_comandos = no

        if def_const:
            self.visitar(def_const)

        if def_tipos:
            self.visitar(def_tipos)

        if def_var:
            self.visitar(def_var)

        if lista_func:
            for funcao in lista_func:
                self.visitar(funcao)

        if lista_comandos:
            for comando in lista_comandos:
                self.visitar(comando)

    def visitar_def_const(self, no):
        _, lista_const = no
        for constante in lista_const:
            self.visitar(constante)

    def visitar_constante(self, no):
        _, nome, valor = no

        if self.tabela.existe_no_escopo_atual(nome):
            self.adicionar_erro(
                f"Constante '{nome}' já declarada no escopo {self.tabela.escopo_atual}"
            )
            return

        tipo = self.inferir_tipo_literal(valor)

        self.tabela.adicionar(nome, "constante", tipo, valor=valor)

    def visitar_def_tipos(self, no):
        _, lista_tipos = no
        for tipo in lista_tipos:
            self.visitar(tipo)

    def visitar_tipo(self, no):
        _, nome, tipo_dado = no

        if self.tabela.existe_no_escopo_atual(nome):
            self.adicionar_erro(
                f"Tipo '{nome}' já declarado no escopo {self.tabela.escopo_atual}"
            )
            return

        tipo_info = self.processar_tipo_dado(tipo_dado)

        simbolo = self.tabela.adicionar(nome, "tipo", tipo_info["tipo"])
        if simbolo:
            if "dimensoes" in tipo_info:
                simbolo.dimensoes = tipo_info["dimensoes"]
            if "campos" in tipo_info:
                simbolo.campos = tipo_info["campos"]

    def processar_tipo_dado(self, tipo_dado):
        if isinstance(tipo_dado, str):
            tipo_upper = tipo_dado.upper()
            if tipo_upper in self.tipos_basicos:
                return {"tipo": tipo_upper.lower()}
            else:
                simbolo = self.tabela.buscar(tipo_dado)
                if simbolo and simbolo.classificacao == "tipo":
                    return {"tipo": tipo_dado}
                else:
                    self.adicionar_erro(f"Tipo '{tipo_dado}' não declarado")
                    return {"tipo": "unknown"}

        elif isinstance(tipo_dado, tuple):
            if tipo_dado[0] == "ARRAY":
                _, tamanho, tipo_elem = tipo_dado
                tipo_elem_info = self.processar_tipo_dado(tipo_elem)
                return {
                    "tipo": "array",
                    "tipo_elemento": tipo_elem_info["tipo"],
                    "dimensoes": [tamanho],
                }

            elif tipo_dado[0] == "RECORD":
                _, lista_var = tipo_dado
                campos = {}
                for var in lista_var:
                    _, lista_id, tipo = var
                    tipo_info = self.processar_tipo_dado(tipo)
                    for id_nome in lista_id:
                        campos[id_nome] = tipo_info["tipo"]
                return {"tipo": "record", "campos": campos}

        return {"tipo": "unknown"}

    def visitar_def_var(self, no):
        _, lista_var = no
        for var in lista_var:
            self.visitar(var)

    def visitar_variavel(self, no):
        _, lista_id, tipo_dado = no

        tipo_info = self.processar_tipo_dado(tipo_dado)

        for id_nome in lista_id:
            if self.tabela.existe_no_escopo_atual(id_nome):
                self.adicionar_erro(
                    f"Variável '{id_nome}' já declarada no escopo {self.tabela.escopo_atual}"
                )
                continue

            simbolo = self.tabela.adicionar(id_nome, "variavel", tipo_info["tipo"])
            if simbolo:
                if "dimensoes" in tipo_info:
                    simbolo.dimensoes = tipo_info["dimensoes"]
                if "campos" in tipo_info:
                    simbolo.campos = tipo_info["campos"]

    def visitar_funcao(self, no):
        _, nome, lista_param, tipo_retorno, def_var, lista_comandos = no

        if self.tabela.existe_no_escopo_atual(nome):
            self.adicionar_erro(
                f"Função '{nome}' já declarada no escopo {self.tabela.escopo_atual}"
            )
            return

        tipo_ret_info = self.processar_tipo_dado(tipo_retorno)

        parametros = []
        if lista_param:
            for param in lista_param:
                if param and param[0] == "PARAMETRO":
                    _, lista_id, tipo_param = param
                    tipo_param_info = self.processar_tipo_dado(tipo_param)
                    for id_nome in lista_id:
                        parametros.append((tipo_param_info["tipo"], id_nome))

        simbolo = self.tabela.adicionar(
            nome,
            "funcao",
            tipo_ret_info["tipo"],
            parametros=parametros,
            tipo_retorno=tipo_ret_info["tipo"],
        )

        self.tabela.entrar_escopo(nome)
        self.funcao_atual = nome

        ordem = 1
        if lista_param:
            for param in lista_param:
                if param and param[0] == "PARAMETRO":
                    _, lista_id, tipo_param = param
                    tipo_param_info = self.processar_tipo_dado(tipo_param)
                    for id_nome in lista_id:
                        self.tabela.adicionar(
                            id_nome, "parametro", tipo_param_info["tipo"], ordem=ordem
                        )
                        ordem += 1

        if def_var:
            self.visitar(def_var)

        if lista_comandos:
            for comando in lista_comandos:
                self.visitar(comando)

        self.tabela.sair_escopo()
        self.funcao_atual = None

    def visitar_atribuicao(self, no):
        _, lvalue, expressao = no

        tipo_lvalue = self.obter_tipo_lvalue(lvalue)

        tipo_expr = self.obter_tipo_expressao(expressao)

        if tipo_lvalue and tipo_expr:
            if not self.tipos_compativeis(tipo_lvalue, tipo_expr):
                self.adicionar_erro(
                    f"Tipos incompatíveis em atribuição: "
                    f"não é possível atribuir {tipo_expr} a {tipo_lvalue}"
                )

    def visitar_while(self, no):
        _, condicao, lista_comandos = no

        tipo_cond = self.obter_tipo_expressao(condicao)
        if tipo_cond and tipo_cond != "boolean":
            self.adicionar_erro(
                f"Condição de WHILE deve ser booleana, mas é {tipo_cond}"
            )

        for comando in lista_comandos:
            self.visitar(comando)

    def visitar_if(self, no):
        _, condicao, comandos_then, else_parte = no

        tipo_cond = self.obter_tipo_expressao(condicao)
        if tipo_cond and tipo_cond != "boolean":
            self.adicionar_erro(f"Condição de IF deve ser booleana, mas é {tipo_cond}")

        for comando in comandos_then:
            self.visitar(comando)

        if else_parte:
            _, comandos_else = else_parte
            for comando in comandos_else:
                self.visitar(comando)

    def visitar_write(self, no):
        _, valor = no
        if isinstance(valor, tuple):
            self.obter_tipo_expressao(valor)

    def visitar_read(self, no):
        _, id_nome = no

        simbolo = self.tabela.buscar(id_nome)
        if not simbolo:
            self.adicionar_erro(f"Variável '{id_nome}' não declarada")
        elif simbolo.classificacao != "variavel":
            self.adicionar_erro(f"'{id_nome}' não é uma variável")

    def obter_tipo_lvalue(self, lvalue):
        if isinstance(lvalue, str):
            simbolo = self.tabela.buscar(lvalue)
            if not simbolo:
                self.adicionar_erro(f"Identificador '{lvalue}' não declarado")
                return None

            if simbolo.classificacao not in ["variavel", "parametro"]:
                self.adicionar_erro(
                    f"'{lvalue}' não pode ser usado em atribuição (não é variável)"
                )
                return None

            return simbolo.tipo

        elif isinstance(lvalue, tuple):
            if lvalue[0] == "ARRAY_ACCESS":
                _, id_nome, indice = lvalue

                simbolo = self.tabela.buscar(id_nome)
                if not simbolo:
                    self.adicionar_erro(f"Array '{id_nome}' não declarado")
                    return None

                tipo_indice = self.obter_tipo_expressao(indice)
                if tipo_indice and tipo_indice != "integer":
                    self.adicionar_erro(
                        f"Índice de array deve ser inteiro, mas é {tipo_indice}"
                    )

                return simbolo.tipo

            elif lvalue[0] == "FIELD_ACCESS":
                _, id_base, campo = lvalue

                if isinstance(id_base, str):
                    simbolo = self.tabela.buscar(id_base)
                    if not simbolo:
                        self.adicionar_erro(f"Registro '{id_base}' não declarado")
                        return None

                    if simbolo.campos and campo in simbolo.campos:
                        return simbolo.campos[campo]
                    else:
                        self.adicionar_erro(f"Campo '{campo}' não existe no registro")
                        return None

        return None

    def obter_tipo_expressao(self, expr):
        if expr is None:
            return None

        if isinstance(expr, (int, float)):
            return "integer" if isinstance(expr, int) else "real"

        if isinstance(expr, str):
            if expr.startswith('"') or expr.startswith("'"):
                return "string"

            simbolo = self.tabela.buscar(expr)
            if not simbolo:
                self.adicionar_erro(f"Identificador '{expr}' não declarado")
                return None
            return simbolo.tipo

        if isinstance(expr, tuple):
            if expr[0] == "OP_ARIT":
                _, op, esq, dir = expr
                tipo_esq = self.obter_tipo_expressao(esq)
                tipo_dir = self.obter_tipo_expressao(dir)

                if tipo_esq and tipo_esq not in ["integer", "real"]:
                    self.adicionar_erro(
                        f"Operando esquerdo de {op} deve ser numérico, mas é {tipo_esq}"
                    )
                if tipo_dir and tipo_dir not in ["integer", "real"]:
                    self.adicionar_erro(
                        f"Operando direito de {op} deve ser numérico, mas é {tipo_dir}"
                    )

                if tipo_esq == "real" or tipo_dir == "real":
                    return "real"
                return "integer"

            elif expr[0] == "OP_COMP":
                _, op, esq, dir = expr
                tipo_esq = self.obter_tipo_expressao(esq)
                tipo_dir = self.obter_tipo_expressao(dir)

                return "boolean"

            elif expr[0] == "ARRAY_ACCESS":
                _, id_nome, indice = expr
                simbolo = self.tabela.buscar(id_nome)
                if not simbolo:
                    self.adicionar_erro(f"Array '{id_nome}' não declarado")
                    return None

                tipo_indice = self.obter_tipo_expressao(indice)
                if tipo_indice and tipo_indice != "integer":
                    self.adicionar_erro(
                        f"Índice de array deve ser inteiro, mas é {tipo_indice}"
                    )

                return simbolo.tipo

            elif expr[0] == "FIELD_ACCESS":
                _, id_base, campo = expr
                simbolo = self.tabela.buscar(id_base)
                if not simbolo:
                    self.adicionar_erro(f"Registro '{id_base}' não declarado")
                    return None

                if simbolo.campos and campo in simbolo.campos:
                    return simbolo.campos[campo]
                else:
                    self.adicionar_erro(f"Campo '{campo}' não existe")
                    return None

            elif expr[0] == "CHAMADA_FUNCAO":
                _, nome, args = expr

                simbolo = self.tabela.buscar(nome)
                if not simbolo:
                    self.adicionar_erro(f"Função '{nome}' não declarada")
                    return None

                if simbolo.classificacao != "funcao":
                    self.adicionar_erro(f"'{nome}' não é uma função")
                    return None

                qtd_esperada = len(simbolo.parametros)
                qtd_recebida = len(args)
                if qtd_esperada != qtd_recebida:
                    self.adicionar_erro(
                        f"Função '{nome}' espera {qtd_esperada} argumentos, "
                        f"mas recebeu {qtd_recebida}"
                    )

                for i, (arg, (tipo_param, _)) in enumerate(
                    zip(args, simbolo.parametros), 1
                ):
                    tipo_arg = self.obter_tipo_expressao(arg)
                    if tipo_arg and not self.tipos_compativeis(tipo_param, tipo_arg):
                        self.adicionar_erro(
                            f"Argumento {i} de '{nome}' incompatível: "
                            f"esperado {tipo_param}, recebido {tipo_arg}"
                        )

                return simbolo.tipo_retorno

        return None

    def inferir_tipo_literal(self, valor):
        if isinstance(valor, int):
            return "integer"
        elif isinstance(valor, float):
            return "real"
        elif isinstance(valor, str):
            return "string"
        return "unknown"

    def tipos_compativeis(self, tipo_destino, tipo_origem):
        if tipo_destino == tipo_origem:
            return True

        if tipo_destino == "real" and tipo_origem == "integer":
            return True

        return False

    def imprimir_erros(self):
        if not self.erros:
            print("Nenhum erro semântico encontrado")
            return

        print(f"\n{len(self.erros)} erro(s) semântico(s) encontrado(s):")
        for erro in self.erros:
            print(f"  ✗ {erro}")

    def imprimir_tabela(self):
        print(self.tabela)


def analisar_semantica(ast, verbose=False):
    analisador = SemanticAnalyzer()
    sucesso = analisador.analisar(ast)

    if verbose:
        analisador.imprimir_tabela()

    analisador.imprimir_erros()

    return sucesso, analisador
