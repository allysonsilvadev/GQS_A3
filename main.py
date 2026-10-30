# Arquivo principal para execução dos casos de teste automatizados
# Projeto: E-commerce Carrefour

import sys

# Importando os módulos que estão dentro da pasta 'tests'
try:
    import tests.test_ct01_busca_valida as ct01
    import tests.test_ct02_erro_digitacao as ct02
except ImportError as e:
    print(f"[Erro] Falha ao importar os módulos de teste. Detalhe: {e}")
    sys.exit(1)

def executar_automacao_completa():
    print("=== Iniciando Automação ===")

    print("\n[Executando] CT-01: Busca Válida")
    # ---------------------------------------------------------
    # CT-01: Busca por palavra-chave válida
    # ---------------------------------------------------------
    try:
        ct01.test_ct01_busca_por_palavra_valida('Geladeira') #ESTA FUNÇÃO RECEBE PARAMETRO DE NOME, FAVOR COLOCAR O NOME DO ITEM A SER PROCURADO!!!!!
    except Exception as e:
        print(f"Falha: {e}")

    print("\n[Executando] CT-02: Busca Inválida")
    # ---------------------------------------------------------
    # CT-02: Busca com erro ortográfico
    # ---------------------------------------------------------   
    try:
        ct02.test_ct02_busca_com_erro_ortografico()
    except Exception as e:
        print(f"Falha: {e}")

if __name__ == "__main__":
    executar_automacao_completa()