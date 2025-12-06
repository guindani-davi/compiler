"""
Gerador de Código Intermediário (3 Endereços)
Percorre a AST em pós-ordem gerando código intermediário
"""


class Instruction:
    """Representa uma instrução de 3 endereços"""

    def __init__(self, op, addr1=None, addr2=None, addr3=None):
        self.op = op
        self.addr1 = addr1
        self.addr2 = addr2
        self.addr3 = addr3

    def __str__(self):
        """Formata instrução para string"""
        parts = [self.op]
        if self.addr1 is not None:
            parts.append(str(self.addr1))
        if self.addr2 is not None:
            parts.append(str(self.addr2))
        if self.addr3 is not None:
            parts.append(str(self.addr3))
        return " ".join(parts)

    def __repr__(self):
        return f"Instruction({self.op}, {self.addr1}, {self.addr2}, {self.addr3})"


class CodeGenerator:
    """Gerador de código intermediário"""

    def __init__(self):
        self.instructions = []  # Lista de instruções geradas
        self.temp_counter = 0  # Contador de variáveis temporárias
        self.label_counter = 0  # Contador de labels

    def gerar(self, ast):
        """
        Gera código intermediário a partir da AST

        Args:
            ast: Árvore sintática

        Returns:
            Lista de instruções
        """
        if ast is None:
            return []

        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0

        self.visitar(ast)

        return self.instructions

    def novo_temp(self):
        """Cria uma nova variável temporária"""
        self.temp_counter += 1
        return f"TEMP{self.temp_counter}"

    def novo_label(self):
        """Cria um novo label"""
        self.label_counter += 1
        return f"LABEL{self.label_counter}"

    def emitir(self, op, addr1=None, addr2=None, addr3=None):
        """Emite uma instrução"""
        instr = Instruction(op, addr1, addr2, addr3)
        self.instructions.append(instr)
        return instr

    def visitar(self, no):
        """
        Visita um nó da AST retornando o endereço do resultado

        Returns:
            Endereço (variável ou temporária) com o resultado
        """
        if no is None:
            return None

        # Se for tupla (nó da AST)
        if isinstance(no, tuple) and len(no) > 0:
            tipo_no = no[0]
            metodo = f"gerar_{tipo_no.lower()}"

            if hasattr(self, metodo):
                return getattr(self, metodo)(no)
            else:
                # Nó desconhecido, visita filhos
                for filho in no[1:]:
                    self.visitar(filho)
                return None

        # Se for lista, visita cada elemento
        elif isinstance(no, list):
            resultado = None
            for item in no:
                resultado = self.visitar(item)
            return resultado

        # Se for valor primitivo, retorna
        else:
            return no

    def gerar_programa(self, no):
        """PROGRAMA: ('PROGRAMA', nome, corpo)"""
        _, nome, corpo = no
        self.visitar(corpo)

    def gerar_corpo(self, no):
        """CORPO: ('CORPO', def_const, def_tipos, def_var, lista_func, lista_comandos)"""
        _, def_const, def_tipos, def_var, lista_func, lista_comandos = no

        # Ignorar constantes, tipos e variáveis (declarações)

        # Processar funções
        if lista_func:
            for funcao in lista_func:
                self.visitar(funcao)

        # Processar comandos do programa principal
        if lista_comandos:
            for comando in lista_comandos:
                self.visitar(comando)

    def gerar_funcao(self, no):
        """FUNCAO: ('FUNCAO', nome, lista_param, tipo_retorno, def_var, lista_comandos)"""
        _, nome, lista_param, tipo_retorno, def_var, lista_comandos = no

        # Label para início da função
        self.emitir("LBL", f"FUNC_{nome}")

        # Processar comandos da função
        if lista_comandos:
            for comando in lista_comandos:
                self.visitar(comando)

        # Retorno implícito ao final
        self.emitir("RET")

    def gerar_atribuicao(self, no):
        """ATRIBUICAO: ('ATRIBUICAO', lvalue, expressao)"""
        _, lvalue, expressao = no

        # Gerar código para expressão
        temp_expr = self.gerar_expressao(expressao)

        # Obter endereço do lvalue
        addr_lvalue = self.processar_lvalue(lvalue)

        # Emitir atribuição
        self.emitir("MOV", addr_lvalue, temp_expr)

    def gerar_while(self, no):
        """WHILE: ('WHILE', condicao, lista_comandos)"""
        _, condicao, lista_comandos = no

        # Labels
        label_ini = self.novo_label()
        label_fim = self.novo_label()

        # LBL LABEL_INI
        self.emitir("LBL", label_ini)

        # Avaliar condição
        temp_cond = self.gerar_expressao(condicao)

        # JMZ LABEL_FIM, TEMP_COND
        self.emitir("JMZ", label_fim, temp_cond)

        # Comandos do bloco
        for comando in lista_comandos:
            self.visitar(comando)

        # JMP LABEL_INI
        self.emitir("JMP", label_ini)

        # LBL LABEL_FIM
        self.emitir("LBL", label_fim)

    def gerar_if(self, no):
        """IF: ('IF', condicao, comandos_then, else_parte)"""
        _, condicao, comandos_then, else_parte = no

        # Avaliar condição
        temp_cond = self.gerar_expressao(condicao)

        if else_parte:
            # IF-THEN-ELSE
            label_else = self.novo_label()
            label_fim = self.novo_label()

            # JMZ LABEL_ELSE, TEMP_COND
            self.emitir("JMZ", label_else, temp_cond)

            # Comandos then
            for comando in comandos_then:
                self.visitar(comando)

            # JMP LABEL_FIM
            self.emitir("JMP", label_fim)

            # LBL LABEL_ELSE
            self.emitir("LBL", label_else)

            # Comandos else
            _, comandos_else = else_parte
            for comando in comandos_else:
                self.visitar(comando)

            # LBL LABEL_FIM
            self.emitir("LBL", label_fim)
        else:
            # IF-THEN apenas
            label_fim = self.novo_label()

            # JMZ LABEL_FIM, TEMP_COND
            self.emitir("JMZ", label_fim, temp_cond)

            # Comandos then
            for comando in comandos_then:
                self.visitar(comando)

            # LBL LABEL_FIM
            self.emitir("LBL", label_fim)

    def gerar_write(self, no):
        """WRITE: ('WRITE', expressao_ou_string)"""
        _, valor = no

        if isinstance(valor, tuple):
            # É uma expressão
            temp = self.gerar_expressao(valor)
            self.emitir("WRITE", temp)
        else:
            # É string literal ou variável
            self.emitir("WRITE", valor)

    def gerar_read(self, no):
        """READ: ('READ', id)"""
        _, id_nome = no
        self.emitir("READ", id_nome)

    def gerar_expressao(self, expr):
        """
        Gera código para uma expressão e retorna endereço do resultado
        """
        if expr is None:
            return None

        # Literal numérico
        if isinstance(expr, (int, float)):
            temp = self.novo_temp()
            self.emitir("MOV", temp, expr)
            return temp

        # String literal ou identificador simples
        if isinstance(expr, str):
            # Se for string literal (com aspas), retorna direto
            if expr.startswith('"') or expr.startswith("'"):
                return expr
            # Se for identificador, retorna
            return expr

        # Tupla (operação)
        if isinstance(expr, tuple):
            tipo_expr = expr[0]

            if tipo_expr == "OP_ARIT":
                # Operação aritmética: ('OP_ARIT', op, esq, dir)
                _, op, esq, dir = expr

                temp_esq = self.gerar_expressao(esq)
                temp_dir = self.gerar_expressao(dir)
                temp_resultado = self.novo_temp()

                # Mapear operador para instrução
                op_map = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV"}

                instr_op = op_map.get(op, "ADD")
                self.emitir(instr_op, temp_resultado, temp_esq, temp_dir)

                return temp_resultado

            elif tipo_expr == "OP_COMP":
                # Operação de comparação: ('OP_COMP', op, esq, dir)
                _, op, esq, dir = expr

                temp_esq = self.gerar_expressao(esq)
                temp_dir = self.gerar_expressao(dir)
                temp_resultado = self.novo_temp()

                # Mapear operador para instrução
                op_map = {">": "GTR", "<": "LES", "=": "EQL", "!": "NEQ"}

                instr_op = op_map.get(op, "EQL")
                self.emitir(instr_op, temp_resultado, temp_esq, temp_dir)

                return temp_resultado

            elif tipo_expr == "ARRAY_ACCESS":
                # Acesso a array: ('ARRAY_ACCESS', id, indice)
                _, id_nome, indice = expr

                temp_indice = self.gerar_expressao(indice)
                temp_resultado = self.novo_temp()

                # Array access: resultado = array[indice]
                # Simplificado: usamos notação array_indice
                self.emitir("MOV", temp_resultado, f"{id_nome}[{temp_indice}]")

                return temp_resultado

            elif tipo_expr == "FIELD_ACCESS":
                # Acesso a campo: ('FIELD_ACCESS', id_base, campo)
                _, id_base, campo = expr

                # Se id_base for tupla, processar primeiro
                if isinstance(id_base, tuple):
                    temp_base = self.gerar_expressao(id_base)
                    base = temp_base
                else:
                    base = id_base

                temp_resultado = self.novo_temp()

                # Field access: resultado = registro.campo
                self.emitir("MOV", temp_resultado, f"{base}.{campo}")

                return temp_resultado

            elif tipo_expr == "CHAMADA_FUNCAO":
                # Chamada de função: ('CHAMADA_FUNCAO', nome, args)
                _, nome, args = expr

                # Empilhar argumentos
                for arg in args:
                    temp_arg = self.gerar_expressao(arg)
                    self.emitir("PUSH", temp_arg)

                # Chamar função
                self.emitir("CALL", nome)

                # Desempilhar resultado
                temp_resultado = self.novo_temp()
                self.emitir("POP", temp_resultado)

                return temp_resultado

        return None

    def processar_lvalue(self, lvalue):
        """Processa lvalue e retorna endereço"""
        if isinstance(lvalue, str):
            # ID simples
            return lvalue

        elif isinstance(lvalue, tuple):
            if lvalue[0] == "ARRAY_ACCESS":
                # Acesso a array: ('ARRAY_ACCESS', id, indice)
                _, id_nome, indice = lvalue
                temp_indice = self.gerar_expressao(indice)
                return f"{id_nome}[{temp_indice}]"

            elif lvalue[0] == "FIELD_ACCESS":
                # Acesso a campo: ('FIELD_ACCESS', id_base, campo)
                _, id_base, campo = lvalue

                if isinstance(id_base, tuple):
                    # Array de registros
                    base = self.processar_lvalue(id_base)
                else:
                    base = id_base

                return f"{base}.{campo}"

        return lvalue

    def imprimir_codigo(self):
        """Imprime o código intermediário gerado"""
        if not self.instructions:
            print("Nenhum código intermediário gerado")
            return

        print("\n" + "=" * 70)
        print("CÓDIGO INTERMEDIÁRIO GERADO")
        print("=" * 70)
        print()

        for i, instr in enumerate(self.instructions, 1):
            print(f"{i:4}: {instr}")

        print()
        print("=" * 70)
        print(f"Total: {len(self.instructions)} instruções")
        print("=" * 70)


def gerar_codigo_intermediario(ast, verbose=True):
    """
    Função auxiliar para geração de código intermediário

    Args:
        ast: Árvore sintática
        verbose: Se True, imprime código gerado

    Returns:
        (lista_instrucoes, gerador)
    """
    gerador = CodeGenerator()
    instrucoes = gerador.gerar(ast)

    if verbose:
        gerador.imprimir_codigo()

    return instrucoes, gerador
