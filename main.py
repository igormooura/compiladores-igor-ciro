from lexer import analisar_lexicamente
from parser import Parser
from semantico import AnalisadorSemantico
from gerador_sam import GeradorSaM


with open("programa.txt", "r", encoding="utf8") as arquivo:
    codigo = arquivo.read()


tokens = analisar_lexicamente(codigo)

print("=== TOKENS ===")

for token in tokens:
    print(token)


parser = Parser(tokens)

arvore = parser.programa()

print("\nParser OK")


semantico = AnalisadorSemantico()

semantico.visitar(arvore)

print("Semântico OK")


gerador = GeradorSaM()

codigo_sam = gerador.gerar(arvore)

print("\n=== CÓDIGO SaM ===")
print(codigo_sam)


with open(
    "programa.sam",
    "w",
    encoding="utf8"
) as arquivo:

    arquivo.write(codigo_sam)

print("\nArquivo programa.sam gerado")