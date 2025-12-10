class Symbol:
    def __init__(self, nome, classificacao, tipo=None, escopo="global", linha=None):
        self.nome = nome
        self.classificacao = (
            classificacao
        )
        self.tipo = tipo 
        self.escopo = escopo  
        self.linha = linha  

        self.parametros = []  
        self.tipo_retorno = None  

        self.ordem = None  

        self.dimensoes = []  

        self.campos = {}  

        self.valor = None

    def __repr__(self):
        return f"Symbol({self.nome}, {self.classificacao}, {self.tipo}, {self.escopo})"


class SymbolTable:
    def __init__(self):
        self.symbols = {} 
        self.escopo_atual = "global"
        self.escopos = ["global"]

    def entrar_escopo(self, nome_escopo):
        self.escopos.append(nome_escopo)
        self.escopo_atual = nome_escopo

    def sair_escopo(self):
        if len(self.escopos) > 1:
            self.escopos.pop()
            self.escopo_atual = self.escopos[-1]

    def adicionar(self, nome, classificacao, tipo=None, linha=None, **kwargs):
        if self.existe_no_escopo_atual(nome):
            return None

        simbolo = Symbol(nome, classificacao, tipo, self.escopo_atual, linha)

        for key, value in kwargs.items():
            if hasattr(simbolo, key):
                setattr(simbolo, key, value)

        if nome not in self.symbols:
            self.symbols[nome] = []
        self.symbols[nome].append(simbolo)

        return simbolo

    def buscar(self, nome, escopo=None):
        if nome not in self.symbols:
            return None

        if escopo is not None:
            for simbolo in self.symbols[nome]:
                if simbolo.escopo == escopo:
                    return simbolo
            return None

        for escopo_busca in reversed(self.escopos):
            for simbolo in self.symbols[nome]:
                if simbolo.escopo == escopo_busca:
                    return simbolo

        return None

    def existe(self, nome):
        return self.buscar(nome) is not None

    def existe_no_escopo_atual(self, nome):
        return self.buscar(nome, self.escopo_atual) is not None

    def atualizar(self, nome, **kwargs):
        simbolo = self.buscar(nome)
        if simbolo is None:
            return False

        for key, value in kwargs.items():
            if hasattr(simbolo, key):
                setattr(simbolo, key, value)

        return True

    def obter_todos_no_escopo(self, escopo=None):
        if escopo is None:
            escopo = self.escopo_atual

        resultado = []
        for lista_simbolos in self.symbols.values():
            for simbolo in lista_simbolos:
                if simbolo.escopo == escopo:
                    resultado.append(simbolo)
        return resultado

    def limpar(self):
        self.symbols = {}
        self.escopo_atual = "global"
        self.escopos = ["global"]

    def __repr__(self):
        linhas = ["Tabela de Símbolos:"]
        linhas.append("-" * 100)
        linhas.append(
            f"{'Nome':<15} {'Classificação':<15} {'Tipo':<15} {'Escopo':<15} {'Linha':<10}"
        )
        linhas.append("-" * 100)

        todos_simbolos = []
        for lista in self.symbols.values():
            todos_simbolos.extend(lista)
        todos_simbolos.sort(key=lambda s: (s.escopo, s.nome))

        for simbolo in todos_simbolos:
            tipo_str = str(simbolo.tipo) if simbolo.tipo else "-"
            linha_str = str(simbolo.linha) if simbolo.linha else "-"
            linhas.append(
                f"{simbolo.nome:<15} {simbolo.classificacao:<15} {tipo_str:<15} {simbolo.escopo:<15} {linha_str:<10}"
            )

            if simbolo.classificacao == "funcao" and simbolo.parametros:
                params_str = ", ".join([f"{p[1]}:{p[0]}" for p in simbolo.parametros])
                linhas.append(f"  → Parâmetros: {params_str}")
                if simbolo.tipo_retorno:
                    linhas.append(f"  → Retorno: {simbolo.tipo_retorno}")

            if simbolo.dimensoes:
                dims_str = ", ".join(map(str, simbolo.dimensoes))
                linhas.append(f"  → Dimensões: [{dims_str}]")

            if simbolo.campos:
                linhas.append(f"  → Campos:")
                for campo, tipo in simbolo.campos.items():
                    linhas.append(f"      {campo}: {tipo}")

        linhas.append("-" * 100)
        return "\n".join(linhas)
