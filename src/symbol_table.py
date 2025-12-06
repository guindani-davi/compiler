"""
Tabela de Símbolos para o Compilador
Armazena informações sobre identificadores: variáveis, constantes, funções, parâmetros, tipos
"""


class Symbol:
    """Representa um símbolo na tabela"""

    def __init__(self, nome, classificacao, tipo=None, escopo="global", linha=None):
        self.nome = nome
        self.classificacao = (
            classificacao  # 'variavel', 'constante', 'funcao', 'parametro', 'tipo'
        )
        self.tipo = tipo  # 'inteiro', 'real', 'booleano', 'caractere', 'void', ou tipo customizado
        self.escopo = escopo  # 'global' ou nome da função/procedimento
        self.linha = linha  # linha onde foi declarado

        # Atributos específicos para funções
        self.parametros = []  # lista de (tipo, nome) para funções
        self.tipo_retorno = None  # tipo de retorno da função

        # Atributos específicos para parâmetros
        self.ordem = None  # ordem na lista de parâmetros (1, 2, 3...)

        # Atributos específicos para arrays
        self.dimensoes = []  # lista de dimensões para arrays

        # Atributos específicos para registros
        self.campos = {}  # dicionário {nome_campo: tipo} para registros

        # Valor para constantes
        self.valor = None

    def __repr__(self):
        return f"Symbol({self.nome}, {self.classificacao}, {self.tipo}, {self.escopo})"


class SymbolTable:
    """Tabela de Símbolos com suporte a escopos"""

    def __init__(self):
        self.symbols = {}  # {nome: [Symbol]} - lista para suportar múltiplos escopos
        self.escopo_atual = "global"
        self.escopos = ["global"]  # pilha de escopos

    def entrar_escopo(self, nome_escopo):
        """Entra em um novo escopo (função/procedimento)"""
        self.escopos.append(nome_escopo)
        self.escopo_atual = nome_escopo

    def sair_escopo(self):
        """Sai do escopo atual"""
        if len(self.escopos) > 1:
            self.escopos.pop()
            self.escopo_atual = self.escopos[-1]

    def adicionar(self, nome, classificacao, tipo=None, linha=None, **kwargs):
        """
        Adiciona um símbolo na tabela

        Args:
            nome: nome do identificador
            classificacao: 'variavel', 'constante', 'funcao', 'parametro', 'tipo'
            tipo: tipo do identificador
            linha: linha onde foi declarado
            **kwargs: atributos adicionais (parametros, dimensoes, campos, etc)

        Returns:
            Symbol criado ou None se já existe
        """
        # Verificar se já existe no escopo atual
        if self.existe_no_escopo_atual(nome):
            return None

        # Criar símbolo
        simbolo = Symbol(nome, classificacao, tipo, self.escopo_atual, linha)

        # Adicionar atributos extras
        for key, value in kwargs.items():
            if hasattr(simbolo, key):
                setattr(simbolo, key, value)

        # Adicionar à tabela
        if nome not in self.symbols:
            self.symbols[nome] = []
        self.symbols[nome].append(simbolo)

        return simbolo

    def buscar(self, nome, escopo=None):
        """
        Busca um símbolo na tabela

        Args:
            nome: nome do identificador
            escopo: escopo específico ou None para buscar do atual até global

        Returns:
            Symbol encontrado ou None
        """
        if nome not in self.symbols:
            return None

        # Se escopo específico foi fornecido
        if escopo is not None:
            for simbolo in self.symbols[nome]:
                if simbolo.escopo == escopo:
                    return simbolo
            return None

        # Buscar do escopo atual até global (precedência)
        for escopo_busca in reversed(self.escopos):
            for simbolo in self.symbols[nome]:
                if simbolo.escopo == escopo_busca:
                    return simbolo

        return None

    def existe(self, nome):
        """Verifica se um identificador existe (em qualquer escopo acessível)"""
        return self.buscar(nome) is not None

    def existe_no_escopo_atual(self, nome):
        """Verifica se um identificador já foi declarado no escopo atual"""
        return self.buscar(nome, self.escopo_atual) is not None

    def atualizar(self, nome, **kwargs):
        """
        Atualiza atributos de um símbolo existente

        Args:
            nome: nome do identificador
            **kwargs: atributos a atualizar

        Returns:
            True se atualizado, False se não encontrado
        """
        simbolo = self.buscar(nome)
        if simbolo is None:
            return False

        for key, value in kwargs.items():
            if hasattr(simbolo, key):
                setattr(simbolo, key, value)

        return True

    def obter_todos_no_escopo(self, escopo=None):
        """Retorna todos os símbolos de um escopo"""
        if escopo is None:
            escopo = self.escopo_atual

        resultado = []
        for lista_simbolos in self.symbols.values():
            for simbolo in lista_simbolos:
                if simbolo.escopo == escopo:
                    resultado.append(simbolo)
        return resultado

    def limpar(self):
        """Limpa toda a tabela"""
        self.symbols = {}
        self.escopo_atual = "global"
        self.escopos = ["global"]

    def __repr__(self):
        """Representação textual da tabela"""
        linhas = ["Tabela de Símbolos:"]
        linhas.append("-" * 100)
        linhas.append(
            f"{'Nome':<15} {'Classificação':<15} {'Tipo':<15} {'Escopo':<15} {'Linha':<10}"
        )
        linhas.append("-" * 100)

        # Ordenar por escopo e nome
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

            # Informações adicionais para funções
            if simbolo.classificacao == "funcao" and simbolo.parametros:
                params_str = ", ".join([f"{p[1]}:{p[0]}" for p in simbolo.parametros])
                linhas.append(f"  → Parâmetros: {params_str}")
                if simbolo.tipo_retorno:
                    linhas.append(f"  → Retorno: {simbolo.tipo_retorno}")

            # Informações adicionais para arrays
            if simbolo.dimensoes:
                dims_str = ", ".join(map(str, simbolo.dimensoes))
                linhas.append(f"  → Dimensões: [{dims_str}]")

            # Informações adicionais para registros
            if simbolo.campos:
                linhas.append(f"  → Campos:")
                for campo, tipo in simbolo.campos.items():
                    linhas.append(f"      {campo}: {tipo}")

        linhas.append("-" * 100)
        return "\n".join(linhas)
