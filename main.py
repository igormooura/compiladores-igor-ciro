import sys
import os
from lexer import analisar_lexicamente
from parser import Parser
from semantico import AnalisadorSemantico
from gerador_sam import GeradorSaM


caminho_arquivo = sys.argv[1] if len(sys.argv) > 1 else "programa.txt"

with open(caminho_arquivo, "r", encoding="utf8") as arquivo:
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


caminho_sam = os.path.splitext(caminho_arquivo)[0] + ".sam"
with open(
    caminho_sam,
    "w",
    encoding="utf8"
) as arquivo:

    arquivo.write(codigo_sam)

print(f"\nArquivo {caminho_sam} gerado")