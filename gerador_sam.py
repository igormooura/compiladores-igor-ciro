from ast import *


class GeradorSaM:

    def __init__(self):

        self.codigo = []

        self.variaveis = {}

        self.proximo_offset = 0

        self.contador_rotulos = 0


    def gerar(self, arvore):

        self.visitar(arvore)

        self.codigo.append("STOP")

        return "\n".join(self.codigo)


    def novo_rotulo(self):

        rotulo = f"L{self.contador_rotulos}"

        self.contador_rotulos += 1

        return rotulo


    def visitar(self, no):

        metodo = f"visitar_{type(no).__name__}"

        return getattr(self, metodo)(no)


    def visitar_Programa(self, no):

        for comando in no.comandos:
            self.visitar(comando)


    def visitar_Bloco(self, no):

        for comando in no.comandos:
            self.visitar(comando)


    def visitar_Declaracao(self, no):

        self.variaveis[no.nome] = self.proximo_offset

        self.proximo_offset += 1

        self.codigo.append("PUSHIMM 0")


    def visitar_Atribuicao(self, no):

        self.visitar(no.valor)

        offset = self.variaveis[no.nome]

        self.codigo.append(
            f"STOREOFF {offset}"
        )


    def visitar_Numero(self, no):

        self.codigo.append(
            f"PUSHIMM {no.valor}"
        )


    def visitar_Booleano(self, no):

        valor = 1 if no.valor else 0

        self.codigo.append(
            f"PUSHIMM {valor}"
        )


    def visitar_Variavel(self, no):

        offset = self.variaveis[no.nome]

        self.codigo.append(
            f"PUSHOFF {offset}"
        )


    def visitar_Binario(self, no):

        self.visitar(no.esquerda)

        self.visitar(no.direita)

        if no.operador == "+":
            self.codigo.append("ADD")

        elif no.operador == "-":
            self.codigo.append("SUB")

        elif no.operador == "*":
            self.codigo.append("TIMES")

        elif no.operador == "/":
            self.codigo.append("DIV")

        elif no.operador == "%":
            self.codigo.append("MOD")


    def visitar_Relacional(self, no):

        self.visitar(no.esquerda)

        self.visitar(no.direita)

        if no.operador == ">":
            self.codigo.append("LESS")
 
        elif no.operador == "<":
            self.codigo.append("GREATER")
 
        elif no.operador == "==":
            self.codigo.append("EQUAL")
 
        elif no.operador == "!=":
            self.codigo.append("EQUAL")
            self.codigo.append("NOT")
 
        elif no.operador == ">=":
            self.codigo.append("GREATER")
            self.codigo.append("NOT")
 
        elif no.operador == "<=":
            self.codigo.append("LESS")
            self.codigo.append("NOT")


    def visitar_Logico(self, no):

        self.visitar(no.esquerda)

        self.visitar(no.direita)

        if no.operador == "&&":
            self.codigo.append("AND")

        elif no.operador == "||":
            self.codigo.append("OR")


    def visitar_Negacao(self, no):

        self.visitar(no.expressao)

        self.codigo.append("NOT")


    def visitar_Se(self, no):

        rotulo_senao = self.novo_rotulo()
        rotulo_fim = self.novo_rotulo()

        self.visitar(no.condicao)

        self.codigo.append(
            f"JUMPC {rotulo_senao}"
        )

        self.visitar(no.bloco_se)

        self.codigo.append(
            f"JUMP {rotulo_fim}"
        )

        self.codigo.append(
            f"{rotulo_senao}:"
        )

        if no.bloco_senao:
            self.visitar(no.bloco_senao)

        self.codigo.append(
            f"{rotulo_fim}:"
        )


    def visitar_Enquanto(self, no):

        inicio = self.novo_rotulo()
        fim = self.novo_rotulo()

        self.codigo.append(
            f"{inicio}:"
        )

        self.visitar(no.condicao)

        self.codigo.append(
            f"JUMPC {fim}"
        )

        self.visitar(no.bloco)

        self.codigo.append(
            f"JUMP {inicio}"
        )

        self.codigo.append(
            f"{fim}:"
        )