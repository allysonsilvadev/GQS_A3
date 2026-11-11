# main.py
# Hub centralizador para execução dos casos de teste automatizados
# Projeto: Automação de Testes - E-commerce Demoblaze (Avaliação A3)
# Integrantes: Vinicius Medrades, Allyson da Silva, Diogo Benedik, Rodrigo Cassol

import sys

# =====================================================================
# IMPORTAÇÃO DOS MÓDULOS DE TESTE (PASTA tests/)
# =====================================================================
try:
    import tests.test_ct01_categorias as ct01
    import tests.test_ct02_detalhes_produto as ct02
    
    # Descomente os imports abaixo conforme formos criando os novos arquivos:
    # import tests.test_ct03_adicionar_carrinho as ct03
    # import tests.test_ct04_validar_carrinho as ct04
    # import tests.test_ct05_excluir_carrinho as ct05
    # import tests.test_ct06_ct07_contato as ct_contato  # Mesma função para CT-06 e CT-07
    # import tests.test_ct08_cadastro_existente as ct08
    # import tests.test_ct09_login_invalido as ct09
    # import tests.test_ct10_finalizar_compra as ct10
except ImportError as e:
    print(f"[Erro Crítico] Falha ao importar módulos da pasta 'tests/'. Detalhe: {e}")
    print("Verifique se o arquivo '__init__.py' existe dentro da pasta 'tests/'.")
    sys.exit(1)


def executar_hub_testes():
    print("==========================================================")
    print("   INICIANDO HUB DE AUTOMAÇÃO DE TESTES - DEMOBLAZE (A3)  ")
    print("==========================================================")

    # -----------------------------------------------------------------
    # CT-01: Navegação de Categorias (Ativo - Entrega 2)
    # -----------------------------------------------------------------
    print("\n>>> [Executando] CT-01: Navegação de Categorias")
    try:
        # Teste padrão exigido no CT-01 (Laptops)
        ct01.test_ct01_navegar_categoria(
            categoria="Laptops", 
            produto_esperado="Sony vaio i5"
        )
        # Caso o analista de QA queira testar outra categoria com a mesma função:
        # ct01.test_ct01_navegar_categoria(categoria="Monitors", produto_esperado="Apple monitor 24")
    except Exception as e:
        print(f"[Falha no CT-01]: {e}")

    # -----------------------------------------------------------------
    # CT-02: Visualização de Detalhes do Produto (Ativo - Entrega 2)
    # -----------------------------------------------------------------
    print("\n>>> [Executando] CT-02: Visualização de Detalhes do Produto")
    try:
        ct02.test_ct02_visualizar_detalhes_produto(
            nome_produto="Samsung galaxy s6"
        )
        # Caso o analista de QA queira validar outro produto da vitrine:
        # ct02.test_ct02_visualizar_detalhes_produto(nome_produto="Nokia lumia 1520")
    except Exception as e:
        print(f"[Falha no CT-02]: {e}")

    # -----------------------------------------------------------------
    # CT-03: Adicionar Produto ao Carrinho (Futuro)
    # -----------------------------------------------------------------
    # print("\n>>> [Executando] CT-03: Adicionar Produto ao Carrinho")
    # try:
    #     ct03.test_ct03_adicionar_ao_carrinho(nome_produto="Samsung galaxy s6")
    # except Exception as e:
    #     print(f"[Falha no CT-03]: {e}")

    # -----------------------------------------------------------------
    # CT-04: Validação de Itens no Carrinho (Futuro)
    # -----------------------------------------------------------------
    # print("\n>>> [Executando] CT-04: Validação de Itens no Carrinho")
    # try:
    #     ct04.test_ct04_validar_item_no_carrinho(nome_produto="Samsung galaxy s6")
    # except Exception as e:
    #     print(f"[Falha no CT-04]: {e}")

    # -----------------------------------------------------------------
    # CT-05: Exclusão de Produto do Carrinho (Futuro)
    # -----------------------------------------------------------------
    # print("\n>>> [Executando] CT-05: Exclusão de Produto do Carrinho")
    # try:
    #     ct05.test_ct05_excluir_item_do_carrinho(nome_produto="Samsung galaxy s6")
    # except Exception as e:
    #     print(f"[Falha no CT-05]: {e}")

    # -----------------------------------------------------------------
    # CT-06 e CT-07: Formulário de Contato (Agrupados na mesma função)
    # Requisito A3: Testar sem e com caracteres especiais (ç, ã, etc.)
    # -----------------------------------------------------------------
    # print("\n>>> [Executando] CT-06: Formulário de Contato (Sem Caracteres Especiais)")
    # try:
    #     ct_contato.test_enviar_formulario_contato(
    #         caso_teste="CT-06",
    #         email="qa.teste@exemplo.com",
    #         nome="Rodrigo QA",
    #         mensagem="Duvida sobre disponibilidade do Notebook Y e Celular X"
    #     )
    # except Exception as e:
    #     print(f"[Falha no CT-06]: {e}")

    # print("\n>>> [Executando] CT-07: Formulário de Contato (Com Caracteres Especiais)")
    # try:
    #     ct_contato.test_enviar_formulario_contato(
    #         caso_teste="CT-07",
    #         email="qa.teste@exemplo.com",
    #         nome="João Conceição",
    #         mensagem="Solicitação de cotação e informações de manutenção do aparelho!"
    #     )
    # except Exception as e:
    #     print(f"[Falha no CT-07]: {e}")

    # -----------------------------------------------------------------
    # CT-08: Cadastro de Usuário (Sign up) Bloqueado (Futuro)
    # -----------------------------------------------------------------
    # print("\n>>> [Executando] CT-08: Cadastro de Usuário Já Existente")
    # try:
    #     ct08.test_ct08_cadastro_usuario_existente(usuario="admin", senha="123")
    # except Exception as e:
    #     print(f"[Falha no CT-08]: {e}")

    # -----------------------------------------------------------------
    # CT-09: Login com Credenciais Incorretas (Futuro)
    # -----------------------------------------------------------------
    # print("\n>>> [Executando] CT-09: Login com Credenciais Incorretas")
    # try:
    #     ct09.test_ct09_login_credenciais_invalidas(usuario="usuario_inexistente_qa", senha="000")
    # except Exception as e:
    #     print(f"[Falha no CT-09]: {e}")

    # -----------------------------------------------------------------
    # CT-10: Finalização de Compra - Place Order (Futuro)
    # -----------------------------------------------------------------
    # print("\n>>> [Executando] CT-10: Finalização de Compra (Place Order)")
    # try:
    #     ct10.test_ct10_finalizar_compra(
    #         nome_produto="Samsung galaxy s6",
    #         comprador="Rodrigo Conceição",
    #         pais="Brasil",
    #         cidade="Curitiba",
    #         cartao="1234567812345678",
    #         mes="11",
    #         ano="2026"
    #     )
    # except Exception as e:
    #     print(f"[Falha no CT-10]: {e}")

    print("\n==========================================================")
    print("            EXECUÇÃO DO HUB FINALIZADA                    ")
    print("==========================================================")


if __name__ == "__main__":
    executar_hub_testes()