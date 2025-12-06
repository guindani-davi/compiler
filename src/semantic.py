"""
Analisador Semântico para Pascal Simplificado
Percorre a AST gerada pelo parser e valida regras semânticas
"""

from symbol_table import SymbolTable, Symbol


class SemanticError(Exception):
    """Exceção para erros semânticos"""

    def __init__(self, message, linha=None):
        self.message = message
        self.linha = linha
        super().__init__(self.format_message())

    def format_message(self):
        if self.linha:
            return f"Linha {self.linha}: {self.message}"
        return self.message


class SemanticAnalyzer:
    """Analisador Semântico"""

    def __init__(self):
        self.tabela = SymbolTable()
        self.erros = []
        self.funcao_atual = None  # Para validar RETURN
        self.tipos_basicos = {"INTEGER", "REAL", "BOOLEAN", "CHAR", "STRING"}

    def analisar(self, ast):
        """
        Analisa semanticamente a AST

        Args:
            ast: Árvore sintática retornada pelo parser

        Returns:
            True se sem erros, False caso contrário
        """
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
        """Adiciona um erro à lista"""
        if linha:
            self.erros.append(f"Linha {linha}: {mensagem}")
        else:
            self.erros.append(mensagem)

    def visitar(self, no):
        """Visita um nó da AST"""
        if no is None:
            return None

        # Se for uma tupla (nó da AST)
        if isinstance(no, tuple) and len(no) > 0:
            tipo_no = no[0]
            metodo = f"visitar_{tipo_no.lower()}"

            if hasattr(self, metodo):
                return getattr(self, metodo)(no)
            else:
                # Nó desconhecido, visita filhos
                for filho in no[1:]:
                    self.visitar(filho)
                return None

        # Se for uma lista, visita cada elemento
        elif isinstance(no, list):
            for item in no:
                self.visitar(item)
            return None

        # Se for valor primitivo (int, str, etc), retorna
        else:
            return no

    def visitar_programa(self, no):
        """PROGRAMA: ('PROGRAMA', nome, corpo)"""
        _, nome, corpo = no

        # Adicionar programa à tabela
        self.tabela.adicionar(nome, "programa", "void")

        # Visitar corpo
        self.visitar(corpo)

    def visitar_corpo(self, no):
        """CORPO: ('CORPO', def_const, def_tipos, def_var, lista_func, lista_comandos)"""
        _, def_const, def_tipos, def_var, lista_func, lista_comandos = no

        # Processar constantes
        if def_const:
            self.visitar(def_const)

        # Processar tipos
        if def_tipos:
            self.visitar(def_tipos)

        # Processar variáveis
        if def_var:
            self.visitar(def_var)

        # Processar funções
        if lista_func:
            for funcao in lista_func:
                self.visitar(funcao)

        # Processar comandos do programa principal
        if lista_comandos:
            for comando in lista_comandos:
                self.visitar(comando)

    def visitar_def_const(self, no):
        """DEF_CONST: ('DEF_CONST', lista_const)"""
        _, lista_const = no
        for constante in lista_const:
            self.visitar(constante)

    def visitar_constante(self, no):
        """CONSTANTE: ('CONSTANTE', nome, valor)"""
        _, nome, valor = no

        # Verificar redeclaração
        if self.tabela.existe_no_escopo_atual(nome):
            self.adicionar_erro(
                f"Constante '{nome}' já declarada no escopo {self.tabela.escopo_atual}"
            )
            return

        # Inferir tipo do valor
        tipo = self.inferir_tipo_literal(valor)

        # Adicionar à tabela
        self.tabela.adicionar(nome, "constante", tipo, valor=valor)

    def visitar_def_tipos(self, no):
        """DEF_TIPOS: ('DEF_TIPOS', lista_tipos)"""
        _, lista_tipos = no
        for tipo in lista_tipos:
            self.visitar(tipo)

    def visitar_tipo(self, no):
        """TIPO: ('TIPO', nome, tipo_dado)"""
        _, nome, tipo_dado = no

        # Verificar redeclaração
        if self.tabela.existe_no_escopo_atual(nome):
            self.adicionar_erro(
                f"Tipo '{nome}' já declarado no escopo {self.tabela.escopo_atual}"
            )
            return

        # Processar tipo_dado
        tipo_info = self.processar_tipo_dado(tipo_dado)

        # Adicionar à tabela
        simbolo = self.tabela.adicionar(nome, "tipo", tipo_info["tipo"])
        if simbolo:
            if "dimensoes" in tipo_info:
                simbolo.dimensoes = tipo_info["dimensoes"]
            if "campos" in tipo_info:
                simbolo.campos = tipo_info["campos"]

    def processar_tipo_dado(self, tipo_dado):
        """Processa uma definição de tipo e retorna informações"""
        if isinstance(tipo_dado, str):
            # Tipo simples: INTEGER, REAL, etc ou tipo customizado
            tipo_upper = tipo_dado.upper()
            if tipo_upper in self.tipos_basicos:
                return {"tipo": tipo_upper.lower()}
            else:
                # Tipo customizado - verificar se existe
                simbolo = self.tabela.buscar(tipo_dado)
                if simbolo and simbolo.classificacao == "tipo":
                    return {"tipo": tipo_dado}
                else:
                    self.adicionar_erro(f"Tipo '{tipo_dado}' não declarado")
                    return {"tipo": "unknown"}

        elif isinstance(tipo_dado, tuple):
            if tipo_dado[0] == "ARRAY":
                # ARRAY: ('ARRAY', tamanho, tipo_elemento)
                _, tamanho, tipo_elem = tipo_dado
                tipo_elem_info = self.processar_tipo_dado(tipo_elem)
                return {
                    "tipo": "array",
                    "tipo_elemento": tipo_elem_info["tipo"],
                    "dimensoes": [tamanho],
                }

            elif tipo_dado[0] == "RECORD":
                # RECORD: ('RECORD', lista_var)
                _, lista_var = tipo_dado
                campos = {}
                for var in lista_var:
                    # VARIAVEL: ('VARIAVEL', lista_id, tipo)
                    _, lista_id, tipo = var
                    tipo_info = self.processar_tipo_dado(tipo)
                    for id_nome in lista_id:
                        campos[id_nome] = tipo_info["tipo"]
                return {"tipo": "record", "campos": campos}

        return {"tipo": "unknown"}

    def visitar_def_var(self, no):
        """DEF_VAR: ('DEF_VAR', lista_var)"""
        _, lista_var = no
        for var in lista_var:
            self.visitar(var)

    def visitar_variavel(self, no):
        """VARIAVEL: ('VARIAVEL', lista_id, tipo_dado)"""
        _, lista_id, tipo_dado = no

        # Processar tipo
        tipo_info = self.processar_tipo_dado(tipo_dado)

        # Adicionar cada variável
        for id_nome in lista_id:
            # Verificar redeclaração
            if self.tabela.existe_no_escopo_atual(id_nome):
                self.adicionar_erro(
                    f"Variável '{id_nome}' já declarada no escopo {self.tabela.escopo_atual}"
                )
                continue

            # Adicionar à tabela
            simbolo = self.tabela.adicionar(id_nome, "variavel", tipo_info["tipo"])
            if simbolo:
                if "dimensoes" in tipo_info:
                    simbolo.dimensoes = tipo_info["dimensoes"]
                if "campos" in tipo_info:
                    simbolo.campos = tipo_info["campos"]

    def visitar_funcao(self, no):
        """FUNCAO: ('FUNCAO', nome, lista_param, tipo_retorno, def_var, lista_comandos)"""
        _, nome, lista_param, tipo_retorno, def_var, lista_comandos = no

        # Verificar redeclaração
        if self.tabela.existe_no_escopo_atual(nome):
            self.adicionar_erro(
                f"Função '{nome}' já declarada no escopo {self.tabela.escopo_atual}"
            )
            return

        # Processar tipo de retorno
        tipo_ret_info = self.processar_tipo_dado(tipo_retorno)

        # Processar parâmetros para obter lista
        parametros = []
        if lista_param:
            for param in lista_param:
                if param and param[0] == "PARAMETRO":
                    _, lista_id, tipo_param = param
                    tipo_param_info = self.processar_tipo_dado(tipo_param)
                    for id_nome in lista_id:
                        parametros.append((tipo_param_info["tipo"], id_nome))

        # Adicionar função à tabela global
        simbolo = self.tabela.adicionar(
            nome,
            "funcao",
            tipo_ret_info["tipo"],
            parametros=parametros,
            tipo_retorno=tipo_ret_info["tipo"],
        )

        # Entrar no escopo da função
        self.tabela.entrar_escopo(nome)
        self.funcao_atual = nome

        # Adicionar parâmetros ao escopo local
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

        # Processar variáveis locais
        if def_var:
            self.visitar(def_var)

        # Processar comandos
        if lista_comandos:
            for comando in lista_comandos:
                self.visitar(comando)

        # Sair do escopo da função
        self.tabela.sair_escopo()
        self.funcao_atual = None

    def visitar_atribuicao(self, no):
        """ATRIBUICAO: ('ATRIBUICAO', lvalue, expressao)"""
        _, lvalue, expressao = no

        # Obter tipo do lvalue
        tipo_lvalue = self.obter_tipo_lvalue(lvalue)

        # Obter tipo da expressão
        tipo_expr = self.obter_tipo_expressao(expressao)

        # Verificar compatibilidade
        if tipo_lvalue and tipo_expr:
            if not self.tipos_compativeis(tipo_lvalue, tipo_expr):
                self.adicionar_erro(
                    f"Tipos incompatíveis em atribuição: "
                    f"não é possível atribuir {tipo_expr} a {tipo_lvalue}"
                )

    def visitar_while(self, no):
        """WHILE: ('WHILE', condicao, lista_comandos)"""
        _, condicao, lista_comandos = no

        # Verificar tipo da condição
        tipo_cond = self.obter_tipo_expressao(condicao)
        if tipo_cond and tipo_cond != "boolean":
            self.adicionar_erro(
                f"Condição de WHILE deve ser booleana, mas é {tipo_cond}"
            )

        # Visitar comandos
        for comando in lista_comandos:
            self.visitar(comando)

    def visitar_if(self, no):
        """IF: ('IF', condicao, comandos_then, else_parte)"""
        _, condicao, comandos_then, else_parte = no

        # Verificar tipo da condição
        tipo_cond = self.obter_tipo_expressao(condicao)
        if tipo_cond and tipo_cond != "boolean":
            self.adicionar_erro(f"Condição de IF deve ser booleana, mas é {tipo_cond}")

        # Visitar comandos then
        for comando in comandos_then:
            self.visitar(comando)

        # Visitar comandos else
        if else_parte:
            _, comandos_else = else_parte
            for comando in comandos_else:
                self.visitar(comando)

    def visitar_write(self, no):
        """WRITE: ('WRITE', expressao_ou_string)"""
        _, valor = no
        # Validar que a expressão tem tipo válido
        if isinstance(valor, tuple):
            self.obter_tipo_expressao(valor)

    def visitar_read(self, no):
        """READ: ('READ', id)"""
        _, id_nome = no

        # Verificar se variável existe
        simbolo = self.tabela.buscar(id_nome)
        if not simbolo:
            self.adicionar_erro(f"Variável '{id_nome}' não declarada")
        elif simbolo.classificacao != "variavel":
            self.adicionar_erro(f"'{id_nome}' não é uma variável")

    def obter_tipo_lvalue(self, lvalue):
        """Obtém o tipo de um lvalue"""
        if isinstance(lvalue, str):
            # ID simples
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
                # Acesso a array: ('ARRAY_ACCESS', id, indice)
                _, id_nome, indice = lvalue

                simbolo = self.tabela.buscar(id_nome)
                if not simbolo:
                    self.adicionar_erro(f"Array '{id_nome}' não declarado")
                    return None

                # Verificar tipo do índice
                tipo_indice = self.obter_tipo_expressao(indice)
                if tipo_indice and tipo_indice != "integer":
                    self.adicionar_erro(
                        f"Índice de array deve ser inteiro, mas é {tipo_indice}"
                    )

                # TODO: Retornar tipo do elemento do array
                return simbolo.tipo

            elif lvalue[0] == "FIELD_ACCESS":
                # Acesso a campo: ('FIELD_ACCESS', id, campo)
                _, id_base, campo = lvalue

                # id_base pode ser string ou tupla (array)
                if isinstance(id_base, str):
                    simbolo = self.tabela.buscar(id_base)
                    if not simbolo:
                        self.adicionar_erro(f"Registro '{id_base}' não declarado")
                        return None

                    # TODO: Verificar se é registro e se campo existe
                    if simbolo.campos and campo in simbolo.campos:
                        return simbolo.campos[campo]
                    else:
                        self.adicionar_erro(f"Campo '{campo}' não existe no registro")
                        return None

        return None

    def obter_tipo_expressao(self, expr):
        """Obtém o tipo de uma expressão"""
        if expr is None:
            return None

        # Literal numérico
        if isinstance(expr, (int, float)):
            return "integer" if isinstance(expr, int) else "real"

        # String literal
        if isinstance(expr, str):
            # Pode ser ID ou string
            # Verificar se é string literal (começa e termina com aspas)
            if expr.startswith('"') or expr.startswith("'"):
                return "string"

            # É um identificador
            simbolo = self.tabela.buscar(expr)
            if not simbolo:
                self.adicionar_erro(f"Identificador '{expr}' não declarado")
                return None
            return simbolo.tipo

        # Tupla (operação ou chamada)
        if isinstance(expr, tuple):
            if expr[0] == "OP_ARIT":
                # Operação aritmética: ('OP_ARIT', op, esq, dir)
                _, op, esq, dir = expr
                tipo_esq = self.obter_tipo_expressao(esq)
                tipo_dir = self.obter_tipo_expressao(dir)

                # Verificar tipos numéricos
                if tipo_esq and tipo_esq not in ["integer", "real"]:
                    self.adicionar_erro(
                        f"Operando esquerdo de {op} deve ser numérico, mas é {tipo_esq}"
                    )
                if tipo_dir and tipo_dir not in ["integer", "real"]:
                    self.adicionar_erro(
                        f"Operando direito de {op} deve ser numérico, mas é {tipo_dir}"
                    )

                # Tipo resultante: real se algum for real, senão integer
                if tipo_esq == "real" or tipo_dir == "real":
                    return "real"
                return "integer"

            elif expr[0] == "OP_COMP":
                # Operação de comparação: ('OP_COMP', op, esq, dir)
                _, op, esq, dir = expr
                tipo_esq = self.obter_tipo_expressao(esq)
                tipo_dir = self.obter_tipo_expressao(dir)

                # Operações de comparação retornam boolean
                return "boolean"

            elif expr[0] == "ARRAY_ACCESS":
                # Acesso a array
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
                # Acesso a campo
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
                # Chamada de função: ('CHAMADA_FUNCAO', nome, args)
                _, nome, args = expr

                simbolo = self.tabela.buscar(nome)
                if not simbolo:
                    self.adicionar_erro(f"Função '{nome}' não declarada")
                    return None

                if simbolo.classificacao != "funcao":
                    self.adicionar_erro(f"'{nome}' não é uma função")
                    return None

                # Verificar quantidade de argumentos
                qtd_esperada = len(simbolo.parametros)
                qtd_recebida = len(args)
                if qtd_esperada != qtd_recebida:
                    self.adicionar_erro(
                        f"Função '{nome}' espera {qtd_esperada} argumentos, "
                        f"mas recebeu {qtd_recebida}"
                    )

                # Verificar tipos dos argumentos
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
        """Infere o tipo de um literal"""
        if isinstance(valor, int):
            return "integer"
        elif isinstance(valor, float):
            return "real"
        elif isinstance(valor, str):
            return "string"
        return "unknown"

    def tipos_compativeis(self, tipo_destino, tipo_origem):
        """Verifica se dois tipos são compatíveis"""
        if tipo_destino == tipo_origem:
            return True

        # Conversão implícita: integer -> real
        if tipo_destino == "real" and tipo_origem == "integer":
            return True

        return False

    def imprimir_erros(self):
        """Imprime todos os erros encontrados"""
        if not self.erros:
            print("✓ Nenhum erro semântico encontrado")
            return

        print(f"\n⚠ {len(self.erros)} erro(s) semântico(s) encontrado(s):")
        for erro in self.erros:
            print(f"  ✗ {erro}")

    def imprimir_tabela(self):
        """Imprime a tabela de símbolos"""
        print(self.tabela)


def analisar_semantica(ast, verbose=False):
    """
    Função auxiliar para análise semântica

    Args:
        ast: Árvore sintática
        verbose: Se True, imprime tabela de símbolos

    Returns:
        (sucesso, analisador)
    """
    analisador = SemanticAnalyzer()
    sucesso = analisador.analisar(ast)

    if verbose:
        analisador.imprimir_tabela()

    analisador.imprimir_erros()

    return sucesso, analisador
