# Projeto: Automação de Testes - Demoblaze (Avaliação A3)
# CT-03: Adicionar Produto ao Carrinho

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
    print(f"\n[CT-03] {mensagem}", flush=True)
    time.sleep(1.5)


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

    # Cria o caminho: Evidencias/CT-03/Adicionar_Samsung_Galaxy_S6_Data_Hora
    caminho_pasta = PASTA_EVIDENCIAS / "CT-03" / f"Adicionar_{nome_limpo}_{data_hora}"
    caminho_pasta.mkdir(parents=True, exist_ok=True)

    caminho_readme = caminho_pasta / "README.txt"
    with open(caminho_readme, "w", encoding="utf-8") as f:
        f.write("Detalhes da Execucao - CT-03 (Adicionar Produto ao Carrinho)\n")
        f.write(f"Produto Testado: {nome_produto}\n")
        f.write(f"Data e Hora: {data_hora}\n")
        f.write("Status Inicial: Em execucao...\n")

    return caminho_pasta, caminho_readme


def atualizar_readme_sucesso(caminho_readme, titulo_produto, texto_alerta):
    """Atualiza o README.txt registrando a mensagem exata do alerta capturado."""
    with open(caminho_readme, "a", encoding="utf-8") as f:
        f.write("Resultado Final: SUCESSO. Produto adicionado ao carrinho.\n")
        f.write(f"Produto Confirmado: {titulo_produto}\n")
        f.write(f"Mensagem do Alerta Capturada: '{texto_alerta}'\n")


def test_ct03_adicionar_ao_carrinho(nome_produto="Samsung galaxy s6"):
    """
    Acessa a página de detalhes de um produto no Demoblaze, clica em 'Add to cart'
    e valida se o alerta nativo do navegador exibe a mensagem 'Product added'.
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

        # Print 1: Página inicial com a vitrine
        navegador.save_screenshot(str(pasta_teste / "1_pagina_inicial.png"))

        # 2. Localiza e clica no produto desejado
        link_produto = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[@id='tbodyid']//a[contains(normalize-space(.), '{nome_produto}')]")
            )
        )
        mostrar_etapa(f"Abrindo detalhes do produto '{nome_produto}'...")
        link_produto.click()

        # 3. Aguarda a página de detalhes carregar e localiza o botão "Add to cart"
        WebDriverWait(navegador, 15).until(EC.url_contains("prod.html"))
        titulo_detalhe = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.name"))
        ).text
        botao_adicionar = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(normalize-space(.), 'Add to cart')]")
            )
        )

        # Print 2: Página de detalhes com o botão 'Add to cart' visível antes do clique
        time.sleep(1)
        navegador.save_screenshot(str(pasta_teste / "2_detalhes_antes_adicionar.png"))

        # 4. Clica em "Add to cart" e aguarda o alerta (pop-up nativo do navegador)
        mostrar_etapa("Clicando em 'Add to cart' e aguardando alerta de confirmação...")
        botao_adicionar.click()

        alerta = WebDriverWait(navegador, 15).until(EC.alert_is_present())
        texto_alerta = alerta.text
        mostrar_etapa(f"Alerta capturado: '{texto_alerta}'")

        # 5. Valida a mensagem do alerta e confirma (aceita o pop-up)
        assert "product added" in texto_alerta.lower(), (
            f"Mensagem inesperada no alerta: '{texto_alerta}'"
        )
        alerta.accept()

        # Print 3: Tela após aceitar o alerta (o Selenium bloqueia prints enquanto um alert nativo está aberto)
        time.sleep(1)
        navegador.save_screenshot(str(pasta_teste / "3_apos_confirmar_alerta.png"))

        atualizar_readme_sucesso(caminho_readme, titulo_detalhe, texto_alerta)
        print(f"\n[SUCESSO] Evidências e README salvos na pasta:\n{pasta_teste}")

    finally:
        print("\nFechando o navegador em 2 segundos...", flush=True)
        time.sleep(2)
        navegador.quit()


if __name__ == "__main__":
    # Permite testar este arquivo individualmente se desejar
    test_ct03_adicionar_ao_carrinho("Samsung galaxy s6")