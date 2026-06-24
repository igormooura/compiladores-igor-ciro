class Programa:
    def __init__(self, comandos):
        self.comandos = comandos


class Declaracao:
    def __init__(self, tipo, nome, tamanho=None):
        self.tipo = tipo
        self.nome = nome
        self.tamanho = tamanho


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
 
class StringLiteral:
    def __init__(self, valor):
        self.valor = valor
 
 
class CaractereLiteral:
    def __init__(self, valor):
        self.valor = valor
 
 
class AcessoVetor:
    def __init__(self, nome, indice):
        self.nome = nome
        self.indice = indice
 
 
class Funcao:
    def __init__(
        self,
        tipo_retorno,
        nome,
        parametros,
        bloco
    ):
        self.tipo_retorno = tipo_retorno
        self.nome = nome
        self.parametros = parametros
        self.bloco = bloco


class Parametro:
    def __init__(self, tipo, nome):
        self.tipo = tipo
        self.nome = nome


class Retorne:
    def __init__(self, valor):
        self.valor = valor
 
 
class ChamadaFuncao:
    def __init__(self, nome, argumentos):
        self.nome = nome
        self.argumentos = argumentos


class Logico:
    def __init__(self, operador, esquerda, direita):
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita


class Negacao:
    def __init__(self, expressao):
        self.expressao = expressao


class DoEnquanto:
    def __init__(self, bloco, condicao):
        self.bloco = bloco
        self.condicao = condicao


class DeclaracaoConstante:
    def __init__(self, tipo, nome, valor):
        self.tipo = tipo
        self.nome = nome
        self.valor = valor
