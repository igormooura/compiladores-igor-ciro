from ast import *


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0


    def atual(self):

        if self.pos < len(self.tokens):
            return self.tokens[self.pos]

        return None


    def consumir(self, tipo):

        token = self.atual()

        if token is None:
            raise Exception("Fim inesperado do arquivo")

        if token.tipo != tipo:
            raise Exception(
                f"Esperado {tipo}, encontrado {token.tipo}"
            )

        self.pos += 1

        return token


    def programa(self):

        comandos = []

        while self.atual() is not None:
            comandos.append(
                self.comando()
            )

        return Programa(comandos)


    def comando(self):

        token = self.atual()

        if token.tipo in ["INTEIRO", "RACIONAL", "LETRA"]:
            return self.declaracao()

        if token.tipo == "ID":
            return self.atribuicao()

        if token.tipo == "SE":
            return self.se()

        if token.tipo == "ENQUANTO":
            return self.enquanto()

        raise Exception(
            f"Comando inválido: {token.tipo}"
        )


    def declaracao(self):

        tipo = self.atual().valor
        self.pos += 1

        nome = self.consumir("ID").valor

        self.consumir("PONTO_VIRGULA")

        return Declaracao(tipo, nome)


    def atribuicao(self):

        nome = self.consumir("ID").valor

        self.consumir("ATRIBUI")

        valor = self.expressao_relacional()

        self.consumir("PONTO_VIRGULA")

        return Atribuicao(nome, valor)


    def se(self):

        self.consumir("SE")

        self.consumir("ABRE_PAR")

        condicao = self.expressao_relacional()

        self.consumir("FECHA_PAR")

        bloco_se = self.bloco()

        bloco_senao = None

        if (
            self.atual() is not None
            and self.atual().tipo == "SENAO"
        ):
            self.consumir("SENAO")
            bloco_senao = self.bloco()

        return Se(
            condicao,
            bloco_se,
            bloco_senao
        )


    def enquanto(self):

        self.consumir("ENQUANTO")

        self.consumir("ABRE_PAR")

        condicao = self.expressao_relacional()

        self.consumir("FECHA_PAR")

        bloco = self.bloco()

        return Enquanto(
            condicao,
            bloco
        )


    def bloco(self):

        self.consumir("ABRE_CHAVE")

        comandos = []

        while self.atual().tipo != "FECHA_CHAVE":
            comandos.append(
                self.comando()
            )

        self.consumir("FECHA_CHAVE")

        return Bloco(comandos)


    def expressao_relacional(self):

        esquerda = self.expressao()

        if (
            self.atual() is not None
            and self.atual().tipo in [
                "MAIOR",
                "MENOR",
                "MAIOR_IGUAL",
                "MENOR_IGUAL",
                "IGUAL",
                "DIFERENTE"
            ]
        ):

            operador = self.atual().valor

            self.pos += 1

            direita = self.expressao()

            return Relacional(
                operador,
                esquerda,
                direita
            )

        return esquerda


    def expressao(self):

        esquerda = self.termo()

        while (
            self.atual() is not None
            and self.atual().tipo in [
                "SOMA",
                "SUBTRAI"
            ]
        ):

            operador = self.atual().valor

            self.pos += 1

            direita = self.termo()

            esquerda = Binario(
                operador,
                esquerda,
                direita
            )

        return esquerda


    def termo(self):

        esquerda = self.fator()

        while (
            self.atual() is not None
            and self.atual().tipo in [
                "MULTIPLICA",
                "DIVIDE",
                "RESTO"
            ]
        ):

            operador = self.atual().valor

            self.pos += 1

            direita = self.fator()

            esquerda = Binario(
                operador,
                esquerda,
                direita
            )

        return esquerda


    def fator(self):

        token = self.atual()

        if token.tipo == "NUMERO":
            self.pos += 1
            return Numero(token.valor)

        if token.tipo == "VERDADEIRO":
            self.pos += 1
            return Booleano(True)

        if token.tipo == "FALSO":
            self.pos += 1
            return Booleano(False)

        if token.tipo == "ID":
            self.pos += 1
            return Variavel(token.valor)

        if token.tipo == "ABRE_PAR":

            self.consumir("ABRE_PAR")

            expr = self.expressao_relacional()

            self.consumir("FECHA_PAR")

            return expr

        raise Exception(
            f"Fator inválido: {token.tipo}"
        )