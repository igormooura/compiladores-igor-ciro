class Programa:
    def __init__(self, comandos):
        self.comandos = comandos


class Declaracao:
    def __init__(self, tipo, nome):
        self.tipo = tipo
        self.nome = nome


class Atribuicao:
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor


class Bloco:
    def __init__(self, comandos):
        self.comandos = comandos


class Se:
    def __init__(self, condicao, bloco_se, bloco_senao=None):
        self.condicao = condicao
        self.bloco_se = bloco_se
        self.bloco_senao = bloco_senao


class Enquanto:
    def __init__(self, condicao, bloco):
        self.condicao = condicao
        self.bloco = bloco


class Numero:
    def __init__(self, valor):
        self.valor = valor


class Variavel:
    def __init__(self, nome):
        self.nome = nome


class Binario:
    def __init__(self, operador, esquerda, direita):
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita


class Relacional:
    def __init__(self, operador, esquerda, direita):
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita


class Booleano:
    def __init__(self, valor):
        self.valor = valor