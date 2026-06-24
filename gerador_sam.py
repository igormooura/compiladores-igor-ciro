from cigor_ast import *


class GeradorSaM:

    def __init__(self):
        self.codigo = []
        self.variaveis = {}
        self.tipos = {}
        self.proximo_offset = 0
        self.contador_rotulos = 0
        self.funcao_atual = None

    def gerar(self, arvore):
        self.funcoes = {}
        comandos = []
        for comando in arvore.comandos:
            if isinstance(comando, Funcao):
                self.funcoes[comando.nome] = comando
            else:
                comandos.append(comando)

        for comando in comandos:
            self.visitar(comando)

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
        tipo_normalizado = {
            "In": "inteiro",
            "Rac": "racional",
            "Ch": "letra",
            "Bol": "booleano",
            "Txt": "texto"
        }.get(no.tipo, no.tipo)
        
        self.tipos[no.nome] = tipo_normalizado

        if no.tamanho is None:
            self.proximo_offset += 1
            if tipo_normalizado == "racional":
                self.codigo.append("PUSHIMMF 0.0")
            else:
                self.codigo.append("PUSHIMM 0")
        else:
            tamanho = int(no.tamanho)
            self.tipos[no.nome] = ("vetor", tipo_normalizado)
            init_cmd = "PUSHIMMF 0.0" if tipo_normalizado == "racional" else "PUSHIMM 0"
            for _ in range(tamanho):
                self.codigo.append(init_cmd)
            self.proximo_offset += tamanho

    def visitar_Atribuicao(self, no):
        if isinstance(no.nome, AcessoVetor):
            if not isinstance(no.nome.indice, Numero):
                raise Exception('Geração para acesso a vetor só suporta índice constante')
            base = self.variaveis[no.nome.nome]
            indice = int(no.nome.indice.valor)
            offset = base + indice

            self.visitar(no.valor)
            
            tipo_vetor_elem = self.tipos[no.nome.nome]
            if isinstance(tipo_vetor_elem, tuple):
                tipo_elem = tipo_vetor_elem[1]
            else:
                tipo_elem = tipo_vetor_elem
                
            if tipo_elem == "racional" and no.valor.tipo_inferred == "inteiro":
                self.codigo.append("ITOF")

            self.codigo.append(
                f"STOREOFF {offset}"
            )
        else:
            self.visitar(no.valor)
            
            tipo_var = self.tipos[no.nome]
            if tipo_var == "racional" and no.valor.tipo_inferred == "inteiro":
                self.codigo.append("ITOF")

            offset = self.variaveis[no.nome]
            self.codigo.append(
                f"STOREOFF {offset}"
            )

    def visitar_Numero(self, no):
        if hasattr(no, 'tipo_inferred') and no.tipo_inferred == "racional":
            self.codigo.append(
                f"PUSHIMMF {no.valor}"
            )
        else:
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

    def visitar_AcessoVetor(self, no):
        if not isinstance(no.indice, Numero):
            raise Exception('Geração para acesso a vetor só suporta índice constante')

        base = self.variaveis[no.nome]
        indice = int(no.indice.valor)
        offset = base + indice
        self.codigo.append(f"PUSHOFF {offset}")

    def visitar_Binario(self, no):
        self.visitar(no.esquerda)
        if no.esquerda.tipo_inferred == "inteiro" and no.tipo_inferred == "racional":
            self.codigo.append("ITOF")

        self.visitar(no.direita)
        if no.direita.tipo_inferred == "inteiro" and no.tipo_inferred == "racional":
            self.codigo.append("ITOF")

        is_rational = (no.tipo_inferred == "racional")

        if no.operador == "+":
            self.codigo.append("ADDF" if is_rational else "ADD")
        elif no.operador == "-":
            self.codigo.append("SUBF" if is_rational else "SUB")
        elif no.operador == "*":
            self.codigo.append("TIMESF" if is_rational else "TIMES")
        elif no.operador == "/":
            self.codigo.append("DIVF" if is_rational else "DIV")
        elif no.operador == "%":
            self.codigo.append("MOD")

    def visitar_Relacional(self, no):
        self.visitar(no.esquerda)
        tipo_esq = no.esquerda.tipo_inferred
        tipo_dir = no.direita.tipo_inferred
        is_float_cmp = (tipo_esq == "racional" or tipo_dir == "racional")

        if is_float_cmp and tipo_esq == "inteiro":
            self.codigo.append("ITOF")

        self.visitar(no.direita)
        if is_float_cmp and tipo_dir == "inteiro":
            self.codigo.append("ITOF")

        if is_float_cmp:
            self.codigo.append("CMPF")
            self.codigo.append("PUSHIMM 0")
            if no.operador == "?>":
                self.codigo.append("GREATER")
            elif no.operador == "?<":
                self.codigo.append("LESS")
            elif no.operador == "?=":
                self.codigo.append("EQUAL")
            elif no.operador == "?!=":
                self.codigo.append("EQUAL")
                self.codigo.append("NOT")
            elif no.operador == "?>=":
                self.codigo.append("LESS")
                self.codigo.append("NOT")
            elif no.operador == "?<=":
                self.codigo.append("GREATER")
                self.codigo.append("NOT")
        else:
            if no.operador == "?>":
                self.codigo.append("GREATER")
            elif no.operador == "?<":
                self.codigo.append("LESS")
            elif no.operador == "?=":
                self.codigo.append("EQUAL")
            elif no.operador == "?!=":
                self.codigo.append("EQUAL")
                self.codigo.append("NOT")
            elif no.operador == "?>=":
                self.codigo.append("LESS")
                self.codigo.append("NOT")
            elif no.operador == "?<=":
                self.codigo.append("GREATER")
                self.codigo.append("NOT")

    def visitar_Logico(self, no):
        self.visitar(no.esquerda)
        self.visitar(no.direita)
        if no.operador == "?e":
            self.codigo.append("AND")
        elif no.operador == "?ou":
            self.codigo.append("OR")

    def visitar_Negacao(self, no):
        self.visitar(no.expressao)
        self.codigo.append("NOT")

    def visitar_Se(self, no):
        rotulo_senao = self.novo_rotulo()
        rotulo_fim = self.novo_rotulo()

        self.visitar(no.condicao)
        self.codigo.append("NOT")
        self.codigo.append(f"JUMPC {rotulo_senao}")

        self.visitar(no.bloco_se)
        self.codigo.append(f"JUMP {rotulo_fim}")

        self.codigo.append(f"{rotulo_senao}:")
        if no.bloco_senao:
            self.visitar(no.bloco_senao)

        self.codigo.append(f"{rotulo_fim}:")

    def visitar_Enquanto(self, no):
        inicio = self.novo_rotulo()
        fim = self.novo_rotulo()

        self.codigo.append(f"{inicio}:")
        self.visitar(no.condicao)
        self.codigo.append("NOT")
        self.codigo.append(f"JUMPC {fim}")

        self.visitar(no.bloco)
        self.codigo.append(f"JUMP {inicio}")
        self.codigo.append(f"{fim}:")

    def visitar_DoEnquanto(self, no):
        inicio = self.novo_rotulo()
        fim = self.novo_rotulo()

        self.codigo.append(f"{inicio}:")
        self.visitar(no.bloco)

        self.visitar(no.condicao)
        self.codigo.append("NOT")
        self.codigo.append(f"JUMPC {fim}")
        self.codigo.append(f"JUMP {inicio}")
        self.codigo.append(f"{fim}:")

    def visitar_ChamadaFuncao(self, no):
        if no.nome not in self.funcoes:
            raise Exception(f"Função '{no.nome}' não encontrada para geração")

        func = self.funcoes[no.nome]

        variaveis_antigas = self.variaveis.copy()
        tipos_antigos = self.tipos.copy()
        proximo_antigo = self.proximo_offset
        funcao_atual_antiga = self.funcao_atual
        self.funcao_atual = func

        for parametro, argumento in zip(func.parametros, no.argumentos):
            self.variaveis[parametro.nome] = self.proximo_offset
            self.tipos[parametro.nome] = parametro.tipo
            self.proximo_offset += 1
            
            if parametro.tipo == "racional":
                self.codigo.append("PUSHIMMF 0.0")
            else:
                self.codigo.append("PUSHIMM 0")
            
            self.visitar(argumento)
            if parametro.tipo == "racional" and argumento.tipo_inferred == "inteiro":
                self.codigo.append("ITOF")
            self.codigo.append(f"STOREOFF {self.variaveis[parametro.nome]}")

        for comando in func.bloco.comandos:
            if isinstance(comando, Retorne):
                self.visitar(comando.valor)
                break
            else:
                self.visitar(comando)

        self.variaveis = variaveis_antigas
        self.tipos = tipos_antigos
        self.proximo_offset = proximo_antigo
        self.funcao_atual = funcao_atual_antiga

    def visitar_Retorne(self, no):
        self.visitar(no.valor)
        if self.funcao_atual and self.funcao_atual.tipo_retorno == "racional" and no.valor.tipo_inferred == "inteiro":
            self.codigo.append("ITOF")

    def visitar_DeclaracaoConstante(self, no):
        self.variaveis[no.nome] = self.proximo_offset
        tipo_normalizado = {
            "In": "inteiro",
            "Rac": "racional",
            "Ch": "letra",
            "Bol": "booleano",
            "Txt": "texto"
        }.get(no.tipo, no.tipo)
        
        self.tipos[no.nome] = tipo_normalizado
        self.proximo_offset += 1
        
        self.visitar(no.valor)
        if tipo_normalizado == "racional" and no.valor.tipo_inferred == "inteiro":
            self.codigo.append("ITOF")
