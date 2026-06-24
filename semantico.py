from cigor_ast import *


class TabelaSimbolos:
    def __init__(self):
        self.scopes = [{}]

    def entrar_escopo(self):
        self.scopes.append({})

    def sair_escopo(self):
        self.scopes.pop()

    def declarar(self, nome, tipo):
        if nome in self.scopes[-1]:
            raise Exception(f"Variável '{nome}' já declarada neste escopo")
        self.scopes[-1][nome] = tipo

    def buscar(self, nome):
        for scope in reversed(self.scopes):
            if nome in scope:
                return scope[nome]
        raise Exception(f"Variável '{nome}' não declarada")

    def existe_no_escopo_atual(self, nome):
        return nome in self.scopes[-1]

    def __contains__(self, nome):
        for scope in self.scopes:
            if nome in scope:
                return True
        return False

    def __getitem__(self, nome):
        return self.buscar(nome)

    def __setitem__(self, nome, tipo):
        self.declarar(nome, tipo)


MAPEAMENTO_TIPOS = {
    "In": "inteiro",
    "Rac": "racional",
    "Ch": "letra",
    "Bol": "booleano",
    "Txt": "texto"
}


class AnalisadorSemantico:

    def __init__(self):
        self.tabela = TabelaSimbolos()
        self.funcoes = {}
        self.funcao_atual = None

    def visitar(self, no):
        metodo = f"visitar_{type(no).__name__}"
        if hasattr(self, metodo):
            tipo = getattr(self, metodo)(no)
            if tipo is not None:
                no.tipo_inferred = tipo
            return tipo
        raise Exception(
            f"Semântico não implementado para {type(no).__name__}"
        )

    def visitar_Programa(self, no):
        for comando in no.comandos:
            self.visitar(comando)

    def visitar_Declaracao(self, no):
        if self.tabela.existe_no_escopo_atual(no.nome):
            raise Exception(
                f"Variável '{no.nome}' já declarada neste escopo"
            )
        tipo_normalizado = MAPEAMENTO_TIPOS.get(no.tipo, no.tipo)
        if no.tamanho is None:
            self.tabela[no.nome] = tipo_normalizado
        else:
            # ('vetor', tipo, tamanho)
            self.tabela[no.nome] = ('vetor', tipo_normalizado, no.tamanho)

    def visitar_DeclaracaoConstante(self, no):
        if self.tabela.existe_no_escopo_atual(no.nome):
            raise Exception(
                f"Variável '{no.nome}' já declarada neste escopo"
            )
        tipo_normalizado = MAPEAMENTO_TIPOS.get(no.tipo, no.tipo)
        tipo_valor = self.visitar(no.valor)
        if tipo_normalizado != tipo_valor:
            if tipo_normalizado == "racional" and tipo_valor == "inteiro":
                pass
            else:
                raise Exception(
                    f"Não é possível atribuir {tipo_valor} em constante {tipo_normalizado}"
                )
        self.tabela[no.nome] = ('const', tipo_normalizado)

    def visitar_Atribuicao(self, no):
        if isinstance(no.nome, AcessoVetor):
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
            info = self.tabela[no.nome]
            if isinstance(info, tuple) and info[0] == 'const':
                raise Exception(
                    f"Não é possível alterar o valor da constante '{no.nome}'"
                )
            tipo_variavel = info

        tipo_valor = self.visitar(no.valor)

        if tipo_variavel != tipo_valor:
            if tipo_variavel == "racional" and tipo_valor == "inteiro":
                pass
            else:
                raise Exception(
                    f"Não é possível atribuir {tipo_valor} em {tipo_variavel}"
                )

    def visitar_Variavel(self, no):
        if no.nome not in self.tabela:
            raise Exception(
                f"Variável '{no.nome}' não declarada"
            )
        info = self.tabela[no.nome]
        if isinstance(info, tuple):
            if info[0] == 'vetor':
                raise Exception(f"Uso do vetor '{no.nome}' sem índice")
            elif info[0] == 'const':
                return info[1]
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
            if (tipo_esq == "racional" and tipo_dir == "inteiro") or (tipo_esq == "inteiro" and tipo_dir == "racional"):
                return "racional"
            raise Exception(
                "Tipos incompatíveis em operação aritmética"
            )
        return tipo_esq

    def visitar_Relacional(self, no):
        tipo_esq = self.visitar(no.esquerda)
        tipo_dir = self.visitar(no.direita)

        if tipo_esq != tipo_dir:
            if (tipo_esq == "racional" and tipo_dir == "inteiro") or (tipo_esq == "inteiro" and tipo_dir == "racional"):
                pass
            else:
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

    def visitar_Negativo(self, no):
        tipo = self.visitar(no.expressao)
        if tipo not in ["inteiro", "racional"]:
            raise Exception(
                "Sinal negativo requer valor numérico"
            )
        return tipo

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
        no.tipo_retorno = MAPEAMENTO_TIPOS.get(no.tipo_retorno, no.tipo_retorno)
        self.funcoes[no.nome] = no

        self.tabela.entrar_escopo()
        self.funcao_atual = no

        for parametro in no.parametros:
            if self.tabela.existe_no_escopo_atual(parametro.nome):
                raise Exception(
                    f"Parâmetro '{parametro.nome}' duplicado"
                )
            tipo_param = MAPEAMENTO_TIPOS.get(parametro.tipo, parametro.tipo)
            parametro.tipo = tipo_param
            self.tabela[parametro.nome] = tipo_param

        self.visitar(no.bloco)

        self.tabela.sair_escopo()
        self.funcao_atual = None

    def visitar_Retorne(self, no):
        if self.funcao_atual is None:
            raise Exception(
                "retorne fora de função"
            )
        tipo_retorno = self.visitar(no.valor)

        if tipo_retorno != self.funcao_atual.tipo_retorno:
            if self.funcao_atual.tipo_retorno == "racional" and tipo_retorno == "inteiro":
                pass
            else:
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
                if parametro.tipo == "racional" and tipo_arg == "inteiro":
                    pass
                else:
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
