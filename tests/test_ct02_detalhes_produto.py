# Projeto: Automação de Testes - Demoblaze (Avaliação A3)
# CT-02: Visualização de Detalhes do Produto

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
    print(f"\n[CT-02] {mensagem}", flush=True)
    time.sleep(1.5)


def criar_estrutura_evidencias(nome_produto):
    """Cria a subpasta estruturada com data/hora e o README.txt exigido pela A3."""
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Higieniza o nome do produto para evitar espaços ou caracteres especiais no caminho da pasta
    nome_limpo = nome_produto.replace(" ", "_").replace("ç", "c").replace("ã", "a").title()
    
    # Cria o caminho: Evidencias/CT-02/Detalhes_Samsung_Galaxy_S6_Data_Hora
    caminho_pasta = PASTA_EVIDENCIAS / "CT-02" / f"Detalhes_{nome_limpo}_{data_hora}"
    caminho_pasta.mkdir(parents=True, exist_ok=True)
    
    caminho_readme = caminho_pasta / "README.txt"
    with open(caminho_readme, "w", encoding="utf-8") as f:
        f.write("Detalhes da Execucao - CT-02 (Visualizacao de Detalhes do Produto)\n")
        f.write(f"Produto Selecionado: {nome_produto}\n")
        f.write(f"Data e Hora: {data_hora}\n")
        f.write("Status Inicial: Em execucao...\n")
        
    return caminho_pasta, caminho_readme


def atualizar_readme_sucesso(caminho_readme, titulo_capturado, preco_capturado):
    """Atualiza o README.txt confirmando que os detalhes do produto foram validados."""
    with open(caminho_readme, "a", encoding="utf-8") as f:
        f.write("Resultado Final: SUCESSO. Pagina de detalhes validada (Titulo, Imagem, Preco e Botao).\n")
        f.write(f"Titulo Exibido: {titulo_capturado}\n")
        f.write(f"Preco Exibido: {preco_capturado}\n")


def test_ct02_visualizar_detalhes_produto(nome_produto="Samsung galaxy s6"):
    """
    Acessa a página inicial do Demoblaze, clica em um produto da vitrine
    e valida se a página de detalhes exibe título, imagem, preço e botão 'Add to cart'.
    """
    pasta_teste, caminho_readme = criar_estrutura_evidencias(nome_produto)

    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--window-size=1366,1000")
    navegador = webdriver.Chrome(options=opcoes)

    try:
        # 1. Acessa a página inicial e aguarda os produtos da vitrine carregarem
        navegador.get(SITE)
        WebDriverWait(navegador, 20).until(
            EC.visibility_of_element_located((By.ID, "tbodyid"))
        )
        mostrar_etapa("Página inicial do Demoblaze carregada.")
        
        # Print 1: Página inicial com a vitrine
        navegador.save_screenshot(str(pasta_teste / "1_pagina_inicial.png"))

        # 2. Localiza o produto desejado na vitrine
        link_produto = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[@id='tbodyid']//a[contains(normalize-space(.), '{nome_produto}')]")
            )
        )
        mostrar_etapa(f"Produto '{nome_produto}' localizado na vitrine. Clicando para abrir detalhes...")
        
        # Print 2: Produto localizado antes do clique
        navegador.save_screenshot(str(pasta_teste / "2_produto_na_vitrine.png"))
        link_produto.click()

        # 3. Aguarda o carregamento da página de detalhes (prod.html)
        WebDriverWait(navegador, 15).until(EC.url_contains("prod.html"))
        elemento_titulo = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.name"))
        )

        # 4. Captura e valida título, preço, imagem e botão de compra ("Add to cart")
        titulo_detalhe = elemento_titulo.text
        preco_detalhe = navegador.find_element(By.CSS_SELECTOR, "h3.price-container").text
        imagem_detalhe = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#imgp img"))
        ).get_attribute("src")
        botao_comprar = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(normalize-space(.), 'Add to cart')]"))
        )

        assert nome_produto.lower() in titulo_detalhe.lower(), f"Título incorreto: {titulo_detalhe}"
        assert "$" in preco_detalhe, f"Preço inválido: {preco_detalhe}"
        assert imagem_detalhe, "A imagem do produto não foi carregada na página de detalhes."
        assert botao_comprar.is_displayed(), "O botão 'Add to cart' não está visível."

        mostrar_etapa(f"Detalhes validados! Produto: {titulo_detalhe} | Preço: {preco_detalhe}")
        
        # Print 3: Página de detalhes do produto carregada e validada
        time.sleep(1)
        navegador.save_screenshot(str(pasta_teste / "3_detalhes_produto.png"))
        
        atualizar_readme_sucesso(caminho_readme, titulo_detalhe, preco_detalhe)
        print(f"\n[SUCESSO] Evidências e README salvos na pasta:\n{pasta_teste}")

    finally:
        print("\nFechando o navegador em 2 segundos...", flush=True)
        time.sleep(2)
        navegador.quit()


if __name__ == "__main__":
    # Permite testar este arquivo individualmente se desejar
    test_ct02_visualizar_detalhes_produto("Samsung galaxy s6")