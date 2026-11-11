# Projeto: Automação de Testes - Demoblaze (Avaliação A3)
# CT-01: Navegação de Categorias

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
    print(f"\n[CT-01] {mensagem}", flush=True)
    time.sleep(1.5)


def criar_estrutura_evidencias(categoria_testada, produto_esperado):
    """Cria a subpasta estruturada com data/hora e o README.txt exigido pela A3."""
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Higieniza o nome para evitar espaços ou caracteres especiais no caminho da pasta
    nome_limpo = categoria_testada.replace(" ", "_").replace("ç", "c").replace("ã", "a").title()
    
    # Cria o caminho: Evidencias/CT-01/Categoria_Laptops_Data_Hora
    caminho_pasta = PASTA_EVIDENCIAS / "CT-01" / f"Categoria_{nome_limpo}_{data_hora}"
    caminho_pasta.mkdir(parents=True, exist_ok=True)
    
    caminho_readme = caminho_pasta / "README.txt"
    with open(caminho_readme, "w", encoding="utf-8") as f:
        f.write("Detalhes da Execucao - CT-01 (Navegacao de Categorias)\n")
        f.write(f"Categoria Filtrada: {categoria_testada}\n")
        f.write(f"Produto Validado na Vitrine: {produto_esperado}\n")
        f.write(f"Data e Hora: {data_hora}\n")
        f.write("Status Inicial: Em execucao...\n")
        
    return caminho_pasta, caminho_readme


def atualizar_readme_sucesso(caminho_readme, primeiro_produto, preco):
    """Atualiza o README.txt confirmando que o teste passou."""
    with open(caminho_readme, "a", encoding="utf-8") as f:
        f.write(f"Resultado Final: SUCESSO. Vitrine atualizada corretamente.\n")
        f.write(f"Item Destaque Capturado: {primeiro_produto} ({preco})\n")


def test_ct01_navegar_categoria(categoria="Laptops", produto_esperado="Sony vaio i5"):
    """
    Acessa a página inicial do Demoblaze, filtra por uma categoria do menu lateral
    e valida se os produtos correspondentes são carregados na vitrine.
    """
    pasta_teste, caminho_readme = criar_estrutura_evidencias(categoria, produto_esperado)

    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--window-size=1366,1000")
    navegador = webdriver.Chrome(options=opcoes)

    try:
        # 1. Acessa a página inicial
        navegador.get(SITE)
        WebDriverWait(navegador, 20).until(
            EC.visibility_of_element_located((By.ID, "tbodyid"))
        )
        mostrar_etapa("Página inicial do Demoblaze carregada.")
        
        # Print 1: Página inicial antes do filtro
        navegador.save_screenshot(str(pasta_teste / "1_pagina_inicial.png"))

        # 2. Localiza e clica na categoria desejada no menu lateral
        aba_categoria = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//a[@id='itemc' and contains(normalize-space(.), '{categoria}')]")
            )
        )
        mostrar_etapa(f"Clicando na categoria '{categoria}'...")
        aba_categoria.click()

        # Print 2: Momento logo após acionar o filtro
        time.sleep(1)
        navegador.save_screenshot(str(pasta_teste / "2_categoria_selecionada.png"))

        # 3. Aguarda a vitrine atualizar com o produto esperado daquela categoria
        item_vitrine = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//div[@id='tbodyid']//a[contains(normalize-space(.), '{produto_esperado}')]")
            )
        )

        # 4. Valida os dados do card na vitrine
        card_produto = item_vitrine.find_element(By.XPATH, "./ancestor::div[contains(@class, 'card')]")
        titulo_produto = item_vitrine.text
        preco_produto = card_produto.find_element(By.TAG_NAME, "h5").text
        imagem_produto = card_produto.find_element(By.TAG_NAME, "img").get_attribute("src")

        assert produto_esperado.lower() in titulo_produto.lower(), f"Esperado {produto_esperado}, mas veio {titulo_produto}"
        assert "$" in preco_produto, "Preço não encontrado no formato correto."
        assert imagem_produto, "Imagem do produto não carregou."

        mostrar_etapa(f"Vitrine validada! Produto encontrado: {titulo_produto} | Preço: {preco_produto}")
        
        # Print 3: Vitrine carregada e validada com os produtos da categoria
        navegador.save_screenshot(str(pasta_teste / "3_resultados_vitrine.png"))
        
        atualizar_readme_sucesso(caminho_readme, titulo_produto, preco_produto)
        print(f"\n[SUCESSO] Evidências e README salvos na pasta:\n{pasta_teste}")

    finally:
        print("\nFechando o navegador em 2 segundos...", flush=True)
        time.sleep(2)
        navegador.quit()


if __name__ == "__main__":
    # Permite testar este arquivo individualmente se desejar
    test_ct01_navegar_categoria("Laptops", "Sony vaio i5")