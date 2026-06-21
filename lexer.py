import re

TOKENS = [
    ("INTEIRO", r"\bIn\b"),
    ("RACIONAL", r"\bRac\b"),
    ("LETRA", r"\bCh\b"),
    ("BOOLEANO", r"\bBol\b"),
    ("TEXTO", r"\bTxt\b"),
    
    ("SE", r"\?\?"),
    ("SENAO", r"\!\!"),
    ("ENQUANTO", r"\bEnq\b"),
    ("FACA", r"\!\->"),
    
    ("FUNCAO", r"\bCRIAR\b"),
    ("RETORNE", r"\bVOLTA\b"),
    
    ("VERDADEIRO", r":D"),
    ("FALSO", r":C"),
    
    ("DIFERENTE", r"\?\!="),
    ("MAIOR_IGUAL", r"\?>="),
    ("MENOR_IGUAL", r"\?<="),
    ("IGUAL", r"\?="),
    
    ("E", r"\?e\b"),
    ("OU", r"\?ou\b"),
    ("NAO", r"\?not\b"),
    
    ("MAIOR", r"\?>"),
    ("MENOR", r"\?<"),
    
    ("ATRIBUI", r"=>"),
    
    ("STRING_LITERAL", r'"[^"]*"'),
    ("CARACTERE_LITERAL", r"'[^']'"),
    ("NUMERO", r"\d+(\.\d+)?"),
    ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    
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
    ("PONTO_VIRGULA", r"\."),
    
    ("COMENTARIO", r":3.*"),
    
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