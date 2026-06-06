from ast import *


class GeradorSaM:

    def __init__(self):

        self.codigo = []

        self.variaveis = {}

        self.proximo_offset = 0

        self.contador_rotulos = 0


    def gerar(self, arvore):

        # coletar funções para inline
        self.funcoes = {}
        comandos = []
        for comando in arvore.comandos:
            if isinstance(comando, Funcao):
                self.funcoes[comando.nome] = comando
            else:
                comandos.append(comando)

        # visitar apenas comandos não-função (funções serão inlined quando chamadas)
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

        if no.tamanho is None:
            # variável simples
            self.proximo_offset += 1
            self.codigo.append("PUSHIMM 0")
        else:
            # vetor: aloca várias posições
            tamanho = int(no.tamanho)
            for _ in range(tamanho):
                self.codigo.append("PUSHIMM 0")
            self.proximo_offset += tamanho


    def visitar_Atribuicao(self, no):

        # destino pode ser nome (str) ou AcessoVetor
        if isinstance(no.nome, AcessoVetor):
            # acesso a vetor - índice deve ser número literal para geração simples
            if not isinstance(no.nome.indice, Numero):
                raise Exception('Geração para acesso a vetor só suporta índice constante')
            base = self.variaveis[no.nome.nome]
            indice = int(no.nome.indice.valor)
            offset = base + indice

            self.visitar(no.valor)

            self.codigo.append(
                f"STOREOFF {offset}"
            )
        else:
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

    def visitar_AcessoVetor(self, no):

        # suporte simples: índice constante
        if not isinstance(no.indice, Numero):
            raise Exception('Geração para acesso a vetor só suporta índice constante')

        base = self.variaveis[no.nome]
        indice = int(no.indice.valor)
        offset = base + indice

        self.codigo.append(f"PUSHOFF {offset}")


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
            self.codigo.append("GREATER")
 
        elif no.operador == "<":
            self.codigo.append("LESS")
 
        elif no.operador == "==":
            self.codigo.append("EQUAL")
 
        elif no.operador == "!=":
            self.codigo.append("EQUAL")
            self.codigo.append("NOT")
 
        elif no.operador == ">=":
            self.codigo.append("LESS")
            self.codigo.append("NOT")
 
        elif no.operador == "<=":
            self.codigo.append("GREATER")
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

        # JUMPC na SaM salta quando o topo é verdadeiro; inverter condição para pular quando for falso
        self.codigo.append("NOT")
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

        # inverter para JUMPC (salta quando verdadeiro)
        self.codigo.append("NOT")
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

    def visitar_DoEnquanto(self, no):

        inicio = self.novo_rotulo()
        fim = self.novo_rotulo()

        # bloco executa primeiro
        self.codigo.append(f"{inicio}:")
        self.visitar(no.bloco)

        # depois avalia condição
        self.visitar(no.condicao)
        # inverter para JUMPC
        self.codigo.append("NOT")
        self.codigo.append(f"JUMPC {fim}")
        self.codigo.append(f"JUMP {inicio}")
        self.codigo.append(f"{fim}:")

    def visitar_Funcao(self, no):
        # funções armazenadas em self.funcoes no gerar
        # não emitir código diretamente aqui
        return

    def visitar_ChamadaFuncao(self, no):
        if no.nome not in self.funcoes:
            raise Exception(f"Função '{no.nome}' não encontrada para geração")

        func = self.funcoes[no.nome]

        # salvar estado
        variaveis_antigas = self.variaveis.copy()
        proximo_antigo = self.proximo_offset

        # alocar parâmetros como variáveis temporárias e armazenar argumentos
        for parametro, argumento in zip(func.parametros, no.argumentos):
            self.variaveis[parametro.nome] = self.proximo_offset
            self.proximo_offset += 1
            # reservar espaço
            self.codigo.append("PUSHIMM 0")
            # calcular argumento e armazenar
            self.visitar(argumento)
            self.codigo.append(f"STOREOFF {self.variaveis[parametro.nome]}")

        # inline: executar comandos da função até 'retorne'
        for comando in func.bloco.comandos:
            if isinstance(comando, Retorne):
                # gerar código da expressão de retorno e deixar no topo da pilha
                self.visitar(comando.valor)
                break
            else:
                self.visitar(comando)

        # restaurar estado (variáveis locais/temporárias ficam alocadas na memória, mas nomes retornam ao estado anterior)
        self.variaveis = variaveis_antigas
        self.proximo_offset = proximo_antigo

    def visitar_Retorne(self, no):
        # em chamadas inline, o retorno é tratado diretamente; fora disso, gerar expressão
        self.visitar(no.valor)
