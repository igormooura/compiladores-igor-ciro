import re

TOKENS = [

    ("INTEIRO", r"\binteiro\b"),
    ("RACIONAL", r"\bracional\b"),
    ("LETRA", r"\bletra\b"),
    ("BOOLEANO", r"\bbooleano\b"),
    ("TEXTO", r"\btexto\b"),

    ("SE", r"\bse\b"),
    ("SENAO", r"\bsenao\b"),
    ("ENQUANTO", r"\benquanto\b"),
    ("FACA", r"\bfaca\b"),
 
    ("FUNCAO", r"\bfuncao\b"),
    ("RETORNE", r"\bretorne\b"),

    ("VERDADEIRO", r"\bverdadeiro\b"),
    ("FALSO", r"\bfalso\b"),

    ("STRING_LITERAL", r'"[^"]*"'),
    ("CARACTERE_LITERAL", r"'[^']'"),
    ("NUMERO", r"\d+(\.\d+)?"),

    ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),

    ("IGUAL", r"=="),
    ("DIFERENTE", r"!="),
    ("MAIOR_IGUAL", r">="),
    ("MENOR_IGUAL", r"<="),

    ("E", r"&&"),
    ("OU", r"\|\|"),
    ("NAO", r"!"),

    ("MAIOR", r">"),
    ("MENOR", r"<"),

    ("ATRIBUI", r"="),

    ("SOMA", r"\+"),
    ("SUBTRAI", r"-"),
    ("MULTIPLICA", r"\*"),
    ("DIVIDE", r"/"),
    ("RESTO", r"%"),

    ("ABRE_PAR", r"\("),
    ("FECHA_PAR", r"\)"),
 
    ("ABRE_CHAVE", r"\{"),
    ("FECHA_CHAVE", r"\}"),
 
    ("ABRE_COL", r"\["),
    ("FECHA_COL", r"\]"),

    ("VIRGULA", r","),
    ("PONTO_VIRGULA", r";"),

    ("COMENTARIO", r"//.*"),

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

        if tipo not in ["IGNORAR", "COMENTARIO"]:
            tokens.append(Token(tipo, valor))

        pos = match.end()

    if pos != len(codigo):
        raise Exception(
            f"Erro léxico próximo de '{codigo[pos:]}'"
        )

    return tokens