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

        if token.tipo in [
            "INTEIRO",
            "RACIONAL",
            "LETRA",
            "BOOLEANO",
            "TEXTO"
        ]:
            return self.declaracao()
 
        if token.tipo == "FUNCAO":
            return self.funcao()
 
        if token.tipo == "RETORNE":
            return self.retorne()
 
        if token.tipo == "ID":
            return self.atribuicao()
 
        if token.tipo == "SE":
            return self.se()
 
        if token.tipo == "ENQUANTO":
            return self.enquanto()
 
        if token.tipo == "FACA":
            return self.faca()

        raise Exception(
            f"Comando inválido: {token.tipo}"
        )

    def declaracao(self):
 
        tipo = self.atual().valor
        self.pos += 1
 
        nome = self.consumir("ID").valor
 
        # vetor opcional
        tamanho = None
        if self.atual() is not None and self.atual().tipo == "ABRE_COL":
            self.consumir("ABRE_COL")
            if self.atual().tipo != "NUMERO":
                raise Exception("Tamanho do vetor deve ser número")
            tamanho = int(self.atual().valor)
            self.pos += 1
            self.consumir("FECHA_COL")
 
        self.consumir("PONTO_VIRGULA")
 
        return Declaracao(tipo, nome, tamanho)

    def atribuicao(self):
 
        nome_token = self.consumir("ID")
        nome = nome_token.valor
 
        destino = nome
        if self.atual() is not None and self.atual().tipo == "ABRE_COL":
            self.consumir("ABRE_COL")
            indice = self.expressao_logica()
            self.consumir("FECHA_COL")
            destino = AcessoVetor(nome, indice)
 
        self.consumir("ATRIBUI")
 
        valor = self.expressao_logica()
 
        self.consumir("PONTO_VIRGULA")
 
        return Atribuicao(destino, valor)

    def se(self):

        self.consumir("SE")

        self.consumir("ABRE_PAR")

        condicao = self.expressao_logica()

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

        condicao = self.expressao_logica()

        self.consumir("FECHA_PAR")

        bloco = self.bloco()

        return Enquanto(
            condicao,
            bloco
        )

    def funcao(self):

        self.consumir("FUNCAO")

        tipo = self.atual().valor
        self.pos += 1

        nome = self.consumir("ID").valor

        self.consumir("ABRE_PAR")

        parametros = []

        if self.atual().tipo != "FECHA_PAR":

            parametros.append(
                self.parametro()
            )

            while self.atual().tipo == "VIRGULA":

                self.consumir("VIRGULA")

                parametros.append(
                    self.parametro()
                )

        self.consumir("FECHA_PAR")

        bloco = self.bloco()

        return Funcao(
            tipo,
            nome,
            parametros,
            bloco
        )

    def parametro(self):

        tipo = self.atual().valor
        self.pos += 1

        nome = self.consumir("ID").valor

        return Parametro(
            tipo,
            nome
        )

    def retorne(self):
 
        self.consumir("RETORNE")
 
        valor = self.expressao_logica()
 
        self.consumir("PONTO_VIRGULA")
 
        return Retorne(valor)
 
    def faca(self):
 
        self.consumir("FACA")
 
        bloco = self.bloco()
 
        self.consumir("ENQUANTO")
 
        self.consumir("ABRE_PAR")
 
        condicao = self.expressao_logica()
 
        self.consumir("FECHA_PAR")
 
        self.consumir("PONTO_VIRGULA")
 
        return DoEnquanto(bloco, condicao)
    def bloco(self):

        self.consumir("ABRE_CHAVE")

        comandos = []

        while self.atual().tipo != "FECHA_CHAVE":
            comandos.append(
                self.comando()
            )

        self.consumir("FECHA_CHAVE")

        return Bloco(comandos)

    def expressao_logica(self):

        esquerda = self.expressao_relacional()

        while (
            self.atual() is not None
            and self.atual().tipo in [
                "E",
                "OU"
            ]
        ):

            operador = self.atual().valor

            self.pos += 1

            direita = self.expressao_relacional()

            esquerda = Logico(
                operador,
                esquerda,
                direita
            )

        return esquerda

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

    def chamada_funcao(self):

        nome = self.consumir("ID").valor

        self.consumir("ABRE_PAR")

        argumentos = []

        if self.atual().tipo != "FECHA_PAR":

            argumentos.append(
                self.expressao_logica()
            )

            while self.atual().tipo == "VIRGULA":

                self.consumir("VIRGULA")

                argumentos.append(
                    self.expressao_logica()
                )

        self.consumir("FECHA_PAR")

        return ChamadaFuncao(
            nome,
            argumentos
        )

    def fator(self):
 
        token = self.atual()
 
        if token.tipo == "NUMERO":
            self.pos += 1
            return Numero(token.valor)
 
        if token.tipo == "STRING_LITERAL":
            self.pos += 1
            return StringLiteral(token.valor)
 
        if token.tipo == "CARACTERE_LITERAL":
            self.pos += 1
            return CaractereLiteral(token.valor)
 
        if token.tipo == "VERDADEIRO":
            self.pos += 1
            return Booleano(True)
 
        if token.tipo == "FALSO":
            self.pos += 1
            return Booleano(False)
 
        if token.tipo == "NAO":
 
            self.consumir("NAO")
 
            return Negacao(
                self.fator()
            )
 
        if token.tipo == "ID":
 
            # chamada de funcao
            if (
                self.pos + 1 < len(self.tokens)
                and self.tokens[self.pos + 1].tipo == "ABRE_PAR"
            ):
                return self.chamada_funcao()
 
            # acesso a vetor: id[expr]
            if (
                self.pos + 1 < len(self.tokens)
                and self.tokens[self.pos + 1].tipo == "ABRE_COL"
            ):
                nome = token.valor
                self.pos += 1
                self.consumir("ABRE_COL")
                indice = self.expressao_logica()
                self.consumir("FECHA_COL")
                return AcessoVetor(nome, indice)
 
            self.pos += 1
 
            return Variavel(token.valor)
 
        if token.tipo == "ABRE_PAR":
 
            self.consumir("ABRE_PAR")
 
            expr = self.expressao_logica()
 
            self.consumir("FECHA_PAR")
 
            return expr
 
        raise Exception(
            f"Fator inválido: {token.tipo}"
        )