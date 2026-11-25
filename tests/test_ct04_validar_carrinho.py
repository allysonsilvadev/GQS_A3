# Projeto: Automação de Testes - Demoblaze (Avaliação A3)
# CT-04: Validação de Itens no Carrinho

import re
import time
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SITE = "https://www.demoblaze.com/"
PASTA_EVIDENCIAS = Path(__file__).resolve().parents[1] / "Evidencias"


def mostrar_etapa(mensagem):
    print(f"\n[CT-04] {mensagem}", flush=True)
    time.sleep(1.5)


def extrair_valor_numerico(texto_preco):
    """Extrai apenas os dígitos do preço (ex: '$360 *includes tax' -> '360')."""
    encontrado = re.search(r"\d+", texto_preco)
    return encontrado.group(0) if encontrado else ""


def criar_estrutura_evidencias(nome_produto):
    """Cria a subpasta estruturada com data/hora e o README.txt exigido pela A3."""
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Higieniza o nome do produto para evitar espaços ou caracteres especiais no caminho da pasta
    nome_limpo = (
        nome_produto.replace(" ", "_")
        .replace("ç", "c")
        .replace("ã", "a")
        .title()
    )

    # Cria o caminho: Evidencias/CT-04/Carrinho_Samsung_Galaxy_S6_Data_Hora
    caminho_pasta = PASTA_EVIDENCIAS / "CT-04" / f"Carrinho_{nome_limpo}_{data_hora}"
    caminho_pasta.mkdir(parents=True, exist_ok=True)

    caminho_readme = caminho_pasta / "README.txt"
    with open(caminho_readme, "w", encoding="utf-8") as f:
        f.write("Detalhes da Execucao - CT-04 (Validacao de Itens no Carrinho)\n")
        f.write(f"Produto Testado: {nome_produto}\n")
        f.write(f"Data e Hora: {data_hora}\n")
        f.write("Status Inicial: Em execucao...\n")

    return caminho_pasta, caminho_readme


def atualizar_readme_sucesso(caminho_readme, titulo_tabela, preco_tabela, total_carrinho):
    """Atualiza o README.txt registrando os dados validados na tabela do carrinho."""
    with open(caminho_readme, "a", encoding="utf-8") as f:
        f.write("Resultado Final: SUCESSO. Item validado corretamente na tabela do carrinho.\n")
        f.write(f"Titulo na Tabela: {titulo_tabela}\n")
        f.write(f"Preco na Tabela: ${preco_tabela}\n")
        f.write(f"Total do Carrinho: ${total_carrinho}\n")


def test_ct04_validar_item_no_carrinho(nome_produto="Samsung galaxy s6"):
    """
    Adiciona um produto ao carrinho no Demoblaze, acessa o menu superior 'Cart'
    e valida se o item aparece na tabela com o título, o preço e o total corretos.
    """
    pasta_teste, caminho_readme = criar_estrutura_evidencias(nome_produto)

    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--window-size=1366,1000")
    navegador = webdriver.Chrome(options=opcoes)

    try:
        # 1. Acessa a página inicial e aguarda a vitrine carregar
        navegador.get(SITE)
        WebDriverWait(navegador, 20).until(
            EC.visibility_of_element_located((By.ID, "tbodyid"))
        )
        mostrar_etapa("Página inicial do Demoblaze carregada.")

        # Print 1: Página inicial
        navegador.save_screenshot(str(pasta_teste / "1_pagina_inicial.png"))

        # 2. Localiza e abre o produto escolhido
        link_produto = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[@id='tbodyid']//a[contains(normalize-space(.), '{nome_produto}')]")
            )
        )
        mostrar_etapa(f"Abrindo produto '{nome_produto}' para adicionar ao carrinho...")
        link_produto.click()

        # 3. Captura título e preço na página de detalhes para comparar depois no carrinho
        WebDriverWait(navegador, 15).until(EC.url_contains("prod.html"))
        titulo_esperado = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.name"))
        ).text
        preco_bruto = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h3.price-container"))
        ).text
        preco_esperado = extrair_valor_numerico(preco_bruto)

        # Print 2: Página de detalhes com o preço original
        time.sleep(1)
        navegador.save_screenshot(str(pasta_teste / "2_produto_selecionado.png"))

        # 4. Clica em 'Add to cart' e aceita o alerta de confirmação
        botao_adicionar = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(normalize-space(.), 'Add to cart')]")
            )
        )
        botao_adicionar.click()

        alerta = WebDriverWait(navegador, 15).until(EC.alert_is_present())
        mostrar_etapa(f"Produto adicionado (alerta: '{alerta.text}'). Acessando o carrinho...")
        alerta.accept()

        # 5. Clica no menu superior 'Cart'
        menu_carrinho = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable((By.ID, "cartur"))
        )
        menu_carrinho.click()

        # 6. Aguarda a tabela do carrinho carregar o item e o valor total
        WebDriverWait(navegador, 15).until(EC.url_contains("cart.html"))
        linha_item = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//tbody[@id='tbodyid']/tr[td[contains(normalize-space(.), '{nome_produto}')]]")
            )
        )
        total_carrinho = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.ID, "totalp"))
        ).text.strip()

        # 7. Extrai título (2ª coluna) e preço (3ª coluna) da linha na tabela do carrinho
        colunas = linha_item.find_elements(By.TAG_NAME, "td")
        titulo_tabela = colunas[1].text.strip()
        preco_tabela = colunas[2].text.strip()

        # 8. Validações (título, preço unitário e total)
        assert titulo_esperado.lower() == titulo_tabela.lower(), (
            f"Título divergente! Esperado: '{titulo_esperado}', encontrado: '{titulo_tabela}'"
        )
        assert preco_esperado == preco_tabela, (
            f"Preço divergente! Esperado: '{preco_esperado}', encontrado: '{preco_tabela}'"
        )
        assert preco_esperado == total_carrinho, (
            f"Total divergente! Esperado: '{preco_esperado}', encontrado: '{total_carrinho}'"
        )

        mostrar_etapa(
            f"Carrinho validado! Item: {titulo_tabela} | Preço: ${preco_tabela} | Total: ${total_carrinho}"
        )

        # Print 3: Carrinho carregado com o produto e valor total validados
        time.sleep(1)
        navegador.save_screenshot(str(pasta_teste / "3_item_validado_no_carrinho.png"))

        atualizar_readme_sucesso(caminho_readme, titulo_tabela, preco_tabela, total_carrinho)
        print(f"\n[SUCESSO] Evidências e README salvos na pasta:\n{pasta_teste}")

    finally:
        print("\nFechando o navegador em 2 segundos...", flush=True)
        time.sleep(2)
        navegador.quit()


if __name__ == "__main__":
    # Permite testar este arquivo individualmente se desejar
    test_ct04_validar_item_no_carrinho("Samsung galaxy s6")