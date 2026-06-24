import sys
import os
from lexer import analisar_lexicamente
from parser import Parser
from semantico import AnalisadorSemantico
from gerador_sam import GeradorSaM

TESTS = [
    ("teste_sucesso_1.txt", "SUCESSO"),
    ("teste_sucesso_2.txt", "SUCESSO"),
    ("teste_sucesso_constante.txt", "SUCESSO"),
    ("exemplo_cigor.txt", "SUCESSO"),
    ("teste_erro_lexico.txt", "ERRO LÉXICO"),
    ("teste_erro_sintatico.txt", "ERRO SINTÁTICO"),
    ("teste_erro_semantico_redeclaracao.txt", "ERRO SEMÂNTICO"),
    ("teste_erro_semantico_tipos.txt", "ERRO SEMÂNTICO"),
    ("teste_erro_semantico_constante.txt", "ERRO SEMÂNTICO"),
]

print("=== INICIANDO TESTES DO COMPILADOR CIGOR ===\n")
all_passed = True

for filepath, expected in TESTS:
    if not os.path.exists(filepath):
        print(f"[!] Arquivo não encontrado: {filepath}")
        continue
        
    with open(filepath, "r", encoding="utf8") as f:
        codigo = f.read()
        
    print(f"Testando: {filepath} (Esperado: {expected})")
    try:
        # 1. Lexical
        try:
            tokens = analisar_lexicamente(codigo)
        except Exception as e:
            raise Exception(f"ERRO LÉXICO: {e}")
            
        # 2. Syntax
        try:
            parser = Parser(tokens)
            arvore = parser.programa()
        except Exception as e:
            raise Exception(f"ERRO SINTÁTICO: {e}")
            
        # 3. Semantic
        try:
            semantico = AnalisadorSemantico()
            semantico.visitar(arvore)
        except Exception as e:
            raise Exception(f"ERRO SEMÂNTICO: {e}")
            
        # 4. Code Generation
        try:
            gerador = GeradorSaM()
            codigo_sam = gerador.gerar(arvore)
        except Exception as e:
            raise Exception(f"ERRO DE GERAÇÃO: {e}")
            
        # If we got here, it succeeded!
        if expected == "SUCESSO":
            sam_filename = filepath.replace(".txt", ".sam")
            with open(sam_filename, "w", encoding="utf8") as sam_file:
                sam_file.write(codigo_sam)
            print(f"  [+] PASSOU (Compilado com sucesso! Código SaM salvo em {sam_filename})")
        else:
            print(f"  [-] FALHOU: Compilou mas deveria ter falhado com {expected}")
            all_passed = False
            
    except Exception as e:
        error_msg = str(e)
        if expected in error_msg:
            print(f"  [+] PASSOU (Capturou o erro esperado: {error_msg})")
        else:
            print(f"  [-] FALHOU: Recebeu '{error_msg}' mas esperava '{expected}'")
            all_passed = False
            
    print("-" * 50)

if all_passed:
    print("\n[OK] TODOS OS CASOS DE TESTE PASSARAM!")
    sys.exit(0)
else:
    print("\n[ERRO] ALGUNS CASOS DE TESTE FALHARAM.")
    sys.exit(1)
