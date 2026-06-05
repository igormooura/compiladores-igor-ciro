import re

TOKENS = [
    # Palavras reservadas
    ("INTEIRO", r"\binteiro\b"),
    ("RACIONAL", r"\bracional\b"),
    ("LETRA", r"\bletra\b"),

    ("SE", r"\bse\b"),
    ("SENAO", r"\bsenao\b"),
    ("ENQUANTO", r"\benquanto\b"),

    ("VERDADEIRO", r"\bverdadeiro\b"),
    ("FALSO", r"\bfalso\b"),

    # Literais
    ("NUMERO", r"\d+(\.\d+)?"),
    ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),

    # Relacionais
    ("IGUAL", r"=="),
    ("DIFERENTE", r"!="),
    ("MAIOR_IGUAL", r">="),
    ("MENOR_IGUAL", r"<="),

    ("MAIOR", r">"),
    ("MENOR", r"<"),

    # Lógicos
    ("E", r"&&"),
    ("OU", r"\|\|"),
    ("NAO", r"!"),

    # Atribuição
    ("ATRIBUI", r"="),

    # Aritméticos
    ("SOMA", r"\+"),
    ("SUBTRAI", r"-"),
    ("MULTIPLICA", r"\*"),
    ("DIVIDE", r"/"),
    ("RESTO", r"%"),

    # Símbolos
    ("ABRE_PAR", r"\("),
    ("FECHA_PAR", r"\)"),

    ("ABRE_CHAVE", r"\{"),
    ("FECHA_CHAVE", r"\}"),

    ("VIRGULA", r","),
    ("PONTO_VIRGULA", r";"),

    # Comentários
    ("COMENTARIO", r"//.*"),

    # Espaços
    ("IGNORAR", r"[ \t\n]+"),
]


class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"


PADRAO = "|".join(
    f"(?P<{nome}>{regex})"
    for nome, regex in TOKENS
)


def analisar_lexicamente(codigo):
    tokens = []
    pos = 0

    for match in re.finditer(PADRAO, codigo):

        if match.start() != pos:
            raise Exception(
                f"Erro léxico próximo de '{codigo[pos:match.start()]}'"
            )

        tipo = match.lastgroup
        valor = match.group()

        if tipo not in ("IGNORAR", "COMENTARIO"):
            tokens.append(Token(tipo, valor))

        pos = match.end()

    if pos != len(codigo):
        raise Exception(
            f"Erro léxico próximo de '{codigo[pos:]}'"
        )

    return tokens


codigo = """
inteiro idade;
racional salario;

idade = 20;
salario = 1500.50;

se (idade >= 18) {
    idade = idade + 1;
}

enquanto (idade < 30) {
    idade = idade + 1;
}
"""

tokens = analisar_lexicamente(codigo)

for token in tokens:
    print(token)