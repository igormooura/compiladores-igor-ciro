from ast import *


class AnalisadorSemantico:

    def __init__(self):

        self.tabela = {}

        self.funcoes = {}

        self.funcao_atual = None


    def visitar(self, no):

        metodo = f"visitar_{type(no).__name__}"

        if hasattr(self, metodo):
            return getattr(self, metodo)(no)

        raise Exception(
            f"Semântico não implementado para {type(no).__name__}"
        )


    def visitar_Programa(self, no):

        for comando in no.comandos:
            self.visitar(comando)


    def visitar_Declaracao(self, no):
 
        if no.nome in self.tabela:
            raise Exception(
                f"Variável '{no.nome}' já declarada"
            )
 
        if no.tamanho is None:
            self.tabela[no.nome] = no.tipo
        else:
            # vetor: armazenar como ('vetor', tipo, tamanho)
            self.tabela[no.nome] = ('vetor', no.tipo, no.tamanho)


    def visitar_Atribuicao(self, no):
 
        # destino pode ser nome ou AcessoVetor
        if isinstance(no.nome, AcessoVetor):
            # verifica vetor
            if no.nome.nome not in self.tabela:
                raise Exception(f"Variável '{no.nome.nome}' não declarada")
            info = self.tabela[no.nome.nome]
            if not isinstance(info, tuple) or info[0] != 'vetor':
                raise Exception(f"'{no.nome.nome}' não é um vetor")
            tipo_variavel = info[1]
        else:
            if no.nome not in self.tabela:
                raise Exception(
                    f"Variável '{no.nome}' não declarada"
                )
            tipo_variavel = self.tabela[no.nome]
 
        tipo_valor = self.visitar(no.valor)
 
        if tipo_variavel != tipo_valor:
            raise Exception(
                f"Não é possível atribuir {tipo_valor} em {tipo_variavel}"
            )


    def visitar_Variavel(self, no):
 
        if no.nome not in self.tabela:
            raise Exception(
                f"Variável '{no.nome}' não declarada"
            )
 
        info = self.tabela[no.nome]
        if isinstance(info, tuple) and info[0] == 'vetor':
            raise Exception(f"Uso do vetor '{no.nome}' sem índice")
 
        return info


    def visitar_Numero(self, no):

        if "." in str(no.valor):
            return "racional"

        return "inteiro"


    def visitar_Booleano(self, no):
        return "booleano"


    def visitar_StringLiteral(self, no):
        return "texto"


    def visitar_CaractereLiteral(self, no):
        return "letra"


    def visitar_Binario(self, no):

        tipo_esq = self.visitar(no.esquerda)
        tipo_dir = self.visitar(no.direita)

        if tipo_esq != tipo_dir:
            raise Exception(
                "Tipos incompatíveis em operação aritmética"
            )

        return tipo_esq


    def visitar_Relacional(self, no):

        tipo_esq = self.visitar(no.esquerda)
        tipo_dir = self.visitar(no.direita)

        if tipo_esq != tipo_dir:
            raise Exception(
                "Comparação entre tipos incompatíveis"
            )

        return "booleano"


    def visitar_Logico(self, no):

        tipo_esq = self.visitar(no.esquerda)
        tipo_dir = self.visitar(no.direita)

        if tipo_esq != "booleano":
            raise Exception(
                "Operação lógica requer booleanos"
            )

        if tipo_dir != "booleano":
            raise Exception(
                "Operação lógica requer booleanos"
            )

        return "booleano"


    def visitar_Negacao(self, no):

        tipo = self.visitar(no.expressao)

        if tipo != "booleano":
            raise Exception(
                "Operador ! requer booleano"
            )

        return "booleano"


    def visitar_Bloco(self, no):

        for comando in no.comandos:
            self.visitar(comando)


    def visitar_Se(self, no):

        tipo = self.visitar(no.condicao)

        if tipo != "booleano":
            raise Exception(
                "Condição do se deve ser booleana"
            )

        self.visitar(no.bloco_se)

        if no.bloco_senao:
            self.visitar(no.bloco_senao)


    def visitar_Enquanto(self, no):

        tipo = self.visitar(no.condicao)

        if tipo != "booleano":
            raise Exception(
                "Condição do enquanto deve ser booleana"
            )

        self.visitar(no.bloco)


    def visitar_Funcao(self, no):

        if no.nome in self.funcoes:
            raise Exception(
                f"Função '{no.nome}' já declarada"
            )

        self.funcoes[no.nome] = no

        tabela_antiga = self.tabela.copy()

        self.funcao_atual = no

        for parametro in no.parametros:

            if parametro.nome in self.tabela:
                raise Exception(
                    f"Parâmetro '{parametro.nome}' duplicado"
                )

            self.tabela[parametro.nome] = parametro.tipo

        self.visitar(no.bloco)

        self.tabela = tabela_antiga

        self.funcao_atual = None


    def visitar_Retorne(self, no):

        if self.funcao_atual is None:
            raise Exception(
                "retorne fora de função"
            )

        tipo_retorno = self.visitar(no.valor)

        if tipo_retorno != self.funcao_atual.tipo_retorno:
            raise Exception(
                f"Função espera {self.funcao_atual.tipo_retorno} "
                f"mas retornou {tipo_retorno}"
            )


    def visitar_ChamadaFuncao(self, no):

        if no.nome not in self.funcoes:
            raise Exception(
                f"Função '{no.nome}' não declarada"
            )

        funcao = self.funcoes[no.nome]

        if len(no.argumentos) != len(funcao.parametros):
            raise Exception(
                f"Quantidade incorreta de argumentos em '{no.nome}'"
            )

        for argumento, parametro in zip(
            no.argumentos,
            funcao.parametros
        ):

            tipo_arg = self.visitar(argumento)

            if tipo_arg != parametro.tipo:
                raise Exception(
                    f"Argumento incompatível em '{no.nome}'"
                )

        return funcao.tipo_retorno

    def visitar_AcessoVetor(self, no):

        if no.nome not in self.tabela:
            raise Exception(f"Vetor '{no.nome}' não declarado")

        info = self.tabela[no.nome]

        if not isinstance(info, tuple) or info[0] != 'vetor':
            raise Exception(f"'{no.nome}' não é um vetor")

        tipo_indice = self.visitar(no.indice)

        if tipo_indice != 'inteiro':
            raise Exception('Índice de vetor deve ser inteiro')

        return info[1]

    def visitar_DoEnquanto(self, no):

        tipo = self.visitar(no.condicao)

        if tipo != 'booleano':
            raise Exception('Condição do faça-enquanto deve ser booleana')

        self.visitar(no.bloco)
