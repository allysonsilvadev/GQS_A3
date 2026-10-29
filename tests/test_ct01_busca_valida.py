# Aluno: Allyson da Silva Pereira
# RA: 942516484

import time
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


SITE = "https://www.carrefour.com.br/"
PASTA_EVIDENCIAS = Path(__file__).resolve().parents[1] / "evidencias"


def mostrar_etapa(mensagem):
    print(f"\n{mensagem}", flush=True)
    time.sleep(2)


def aceitar_cookies(navegador):
    botoes = navegador.find_elements(
        By.XPATH,
        "//*[self::button or self::a][contains(normalize-space(.), "
        "'Aceite todos os cookies')]",
    )
    if botoes and botoes[0].is_displayed():
        botoes[0].click()
        mostrar_etapa("Cookies aceitos.")


def preencher_campo(campo, texto):
    campo.clear()
    for caractere in texto:
        campo.send_keys(caractere)
        time.sleep(0.15)


def salvar_evidencia(navegador):
    PASTA_EVIDENCIAS.mkdir(parents=True, exist_ok=True)
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    caminho = PASTA_EVIDENCIAS / f"CT-01_busca_air_fryer_{data_hora}.png"
    assert navegador.save_screenshot(str(caminho)) is True
    assert caminho.is_file()
    print(f"\nEvidência salva em: {caminho}", flush=True)


def test_ct01_busca_por_palavra_valida():
    # Abre o navegador
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--window-size=1366,1000")
    navegador = webdriver.Chrome(options=opcoes)

    try:
        # Acessa o Carrefour
        navegador.get(SITE)
        WebDriverWait(navegador, 30).until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))
        )
        mostrar_etapa("Página inicial do Carrefour carregada.")
        aceitar_cookies(navegador)

        # Pesquisa Air Fryer
        campo_busca = WebDriverWait(navegador, 30).until(
            EC.element_to_be_clickable((By.ID, "busca-cabecalho"))
        )
        campo_busca.click()
        preencher_campo(campo_busca, "Air Fryer")
        mostrar_etapa("Termo preenchido. Vou abrir os resultados.")
        campo_busca.send_keys(Keys.ENTER)

        # Aguarda os resultados
        WebDriverWait(navegador, 30).until(EC.url_contains("/busca/"))
        primeiro_produto = WebDriverWait(navegador, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'a[data-testid="search-product-card"]')
            )
        )

        # Valida título, imagem e preço
        titulo_busca = navegador.find_element(By.TAG_NAME, "h1").text
        titulo_produto = primeiro_produto.find_element(By.TAG_NAME, "h2").text
        imagem = primeiro_produto.find_element(By.TAG_NAME, "img").get_attribute("src")
        preco = primeiro_produto.find_element(
            By.XPATH,
            ".//span[contains(normalize-space(.), 'R$')]",
        ).text

        assert "air fryer" in titulo_busca.lower()
        assert "air fryer" in titulo_produto.lower()
        assert imagem
        assert "R$" in preco

        mostrar_etapa(f"Produto: {titulo_produto} | Preço: {preco}")
        salvar_evidencia(navegador)

    finally:
        # Fecha o navegador
        print("\nFechando o navegador em 2 segundos...", flush=True)
        time.sleep(2)
        navegador.quit()
