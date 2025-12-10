class Instruction:
    def __init__(self, op, addr1=None, addr2=None, addr3=None):
        self.op = op
        self.addr1 = addr1
        self.addr2 = addr2
        self.addr3 = addr3

    def __str__(self):
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
    def __init__(self):
        self.instructions = [] 
        self.temp_counter = 0  
        self.label_counter = 0 

    def gerar(self, ast):
        if ast is None:
            return []

        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0

        self.visitar(ast)

        return self.instructions

    def novo_temp(self):
        self.temp_counter += 1
        return f"TEMP{self.temp_counter}"

    def novo_label(self):
        self.label_counter += 1
        return f"LABEL{self.label_counter}"

    def emitir(self, op, addr1=None, addr2=None, addr3=None):
        instr = Instruction(op, addr1, addr2, addr3)
        self.instructions.append(instr)
        return instr

    def visitar(self, no):
        if no is None:
            return None

        if isinstance(no, tuple) and len(no) > 0:
            tipo_no = no[0]
            metodo = f"gerar_{tipo_no.lower()}"

            if hasattr(self, metodo):
                return getattr(self, metodo)(no)
            else:
                for filho in no[1:]:
                    self.visitar(filho)
                return None

        elif isinstance(no, list):
            resultado = None
            for item in no:
                resultado = self.visitar(item)
            return resultado

        else:
            return no

    def gerar_programa(self, no):
        _, nome, corpo = no
        self.visitar(corpo)

    def gerar_corpo(self, no):
        _, def_const, def_tipos, def_var, lista_func, lista_comandos = no

        if lista_func:
            for funcao in lista_func:
                self.visitar(funcao)

        if lista_comandos:
            for comando in lista_comandos:
                self.visitar(comando)

    def gerar_funcao(self, no):
        _, nome, lista_param, tipo_retorno, def_var, lista_comandos = no

        self.emitir("LBL", f"FUNC_{nome}")

        if lista_comandos:
            for comando in lista_comandos:
                self.visitar(comando)

        self.emitir("RET")

    def gerar_atribuicao(self, no):
        _, lvalue, expressao = no

        temp_expr = self.gerar_expressao(expressao)

        addr_lvalue = self.processar_lvalue(lvalue)

        self.emitir("MOV", addr_lvalue, temp_expr)

    def gerar_while(self, no):
        _, condicao, lista_comandos = no

        label_ini = self.novo_label()
        label_bloco = self.novo_label()
        label_fim = self.novo_label()

        self.emitir("LBL", label_ini)

        temp_cond = self.gerar_expressao(condicao)

        self.emitir("JNZ", label_bloco, temp_cond)

        self.emitir("JMP", label_fim)

        self.emitir("LBL", label_bloco)

        for comando in lista_comandos:
            self.visitar(comando)

        self.emitir("JMP", label_ini)

        self.emitir("LBL", label_fim)

    def gerar_if(self, no):
        _, condicao, comandos_then, else_parte = no

        temp_cond = self.gerar_expressao(condicao)

        if else_parte:
            label_then = self.novo_label()
            label_fim = self.novo_label()

            self.emitir("JNZ", label_then, temp_cond)

            _, comandos_else = else_parte
            for comando in comandos_else:
                self.visitar(comando)

            self.emitir("JMP", label_fim)

            self.emitir("LBL", label_then)

            for comando in comandos_then:
                self.visitar(comando)

            self.emitir("LBL", label_fim)
        else:
            label_then = self.novo_label()
            label_fim = self.novo_label()

            self.emitir("JNZ", label_then, temp_cond)

            self.emitir("JMP", label_fim)

            self.emitir("LBL", label_then)

            for comando in comandos_then:
                self.visitar(comando)

            self.emitir("LBL", label_fim)

    def gerar_write(self, no):
        _, valor = no

        if isinstance(valor, tuple):
            temp = self.gerar_expressao(valor)
            self.emitir("WRITE", temp)
        else:
            self.emitir("WRITE", valor)

    def gerar_read(self, no):
        _, id_nome = no
        self.emitir("READ", id_nome)

    def gerar_expressao(self, expr):
        if expr is None:
            return None

        if isinstance(expr, (int, float)):
            temp = self.novo_temp()
            self.emitir("MOV", temp, expr)
            return temp

        if isinstance(expr, str):
            if expr.startswith('"') or expr.startswith("'"):
                return expr
            return expr

        if isinstance(expr, tuple):
            tipo_expr = expr[0]

            if tipo_expr == "OP_ARIT":
                _, op, esq, dir = expr

                temp_esq = self.gerar_expressao(esq)
                temp_dir = self.gerar_expressao(dir)
                temp_resultado = self.novo_temp()

                op_map = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV"}

                instr_op = op_map.get(op, "ADD")
                self.emitir(instr_op, temp_resultado, temp_esq, temp_dir)

                return temp_resultado

            elif tipo_expr == "OP_COMP":
                _, op, esq, dir = expr

                temp_esq = self.gerar_expressao(esq)
                temp_dir = self.gerar_expressao(dir)
                temp_resultado = self.novo_temp()

                op_map = {">": "GTR", "<": "LES", "=": "EQL", "!": "NEQ"}

                instr_op = op_map.get(op, "EQL")
                self.emitir(instr_op, temp_resultado, temp_esq, temp_dir)

                return temp_resultado

            elif tipo_expr == "ARRAY_ACCESS":
                _, id_nome, indice = expr

                temp_indice = self.gerar_expressao(indice)
                temp_resultado = self.novo_temp()

                self.emitir("MOV", temp_resultado, f"{id_nome}[{temp_indice}]")

                return temp_resultado

            elif tipo_expr == "FIELD_ACCESS":
                _, id_base, campo = expr

                if isinstance(id_base, tuple):
                    temp_base = self.gerar_expressao(id_base)
                    base = temp_base
                else:
                    base = id_base

                temp_resultado = self.novo_temp()

                self.emitir("MOV", temp_resultado, f"{base}.{campo}")

                return temp_resultado

            elif tipo_expr == "CHAMADA_FUNCAO":
                _, nome, args = expr

                for arg in args:
                    temp_arg = self.gerar_expressao(arg)
                    self.emitir("PUSH", temp_arg)

                self.emitir("CALL", nome)

                temp_resultado = self.novo_temp()
                self.emitir("POP", temp_resultado)

                return temp_resultado

        return None

    def processar_lvalue(self, lvalue):
        if isinstance(lvalue, str):
            return lvalue

        elif isinstance(lvalue, tuple):
            if lvalue[0] == "ARRAY_ACCESS":
                _, id_nome, indice = lvalue
                temp_indice = self.gerar_expressao(indice)
                return f"{id_nome}[{temp_indice}]"

            elif lvalue[0] == "FIELD_ACCESS":
                _, id_base, campo = lvalue

                if isinstance(id_base, tuple):
                    base = self.processar_lvalue(id_base)
                else:
                    base = id_base

                return f"{base}.{campo}"

        return lvalue

    def imprimir_codigo(self):
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
    gerador = CodeGenerator()
    instrucoes = gerador.gerar(ast)

    if verbose:
        gerador.imprimir_codigo()

    return instrucoes, gerador
