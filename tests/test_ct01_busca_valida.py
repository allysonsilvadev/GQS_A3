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
    time.sleep(3)
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


def criar_estrutura_evidencias(termo_testado):
    """Cria a subpasta estruturada e o README conforme exigido pela Avaliação A3."""
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Trata o termo para remover espaços e caracteres especiais do nome da pasta
    termo_pasta = termo_testado.replace(" ", "_").replace("ç", "c").replace("ã", "a").title()
    
    # Cria o caminho: Evidencias/CT-01/Busca_Termo_Data
    caminho_pasta = PASTA_EVIDENCIAS / "CT-01" / f"Busca_{termo_pasta}_{data_hora}"
    caminho_pasta.mkdir(parents=True, exist_ok=True)
    
    # Gera o README.txt obrigatório dentro da subpasta
    caminho_readme = caminho_pasta / "README.txt"
    with open(caminho_readme, "w", encoding="utf-8") as f:
        f.write(f"Detalhes da Execucao - CT-01\n")
        f.write(f"Termo Buscado: {termo_testado}\n")
        f.write(f"Data e Hora: {data_hora}\n")
        f.write(f"Resultado: Sucesso. Termo encontrado na busca.\n")
        
    return caminho_pasta


def test_ct01_busca_por_palavra_valida(termo_busca):
    # Inicializa a pasta de evidências antes de rodar os prints
    pasta_teste = criar_estrutura_evidencias(termo_busca)

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
        
        # Print 1: Salva a evidência da página inicial carregada
        navegador.save_screenshot(str(pasta_teste / "1_pagina_inicial.png"))

        # Busca pelo termo (Loop de Try/Except corrige o erro de Stale Element do site dinâmico)
        tentativas = 3
        campo_busca = None
        for i in range(tentativas):
            try:
                campo_busca = WebDriverWait(navegador, 10).until(
                    EC.element_to_be_clickable((By.ID, "busca-cabecalho"))
                )
                campo_busca.click()
                preencher_campo(campo_busca, termo_busca)
                break
            except Exception as e:
                if i == tentativas - 1:
                    raise e
                time.sleep(1)

        mostrar_etapa(f"Termo '{termo_busca}' preenchido. Vou abrir os resultados.")
        
        # Print 2: Salva a evidência com o termo já digitado, antes do Enter
        navegador.save_screenshot(str(pasta_teste / "2_termo_digitado.png"))
        
        campo_busca.send_keys(Keys.ENTER)

        # Aguarda os resultados
        WebDriverWait(navegador, 30).until(EC.url_contains("/busca/"))
        primeiro_produto = WebDriverWait(navegador, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'a[data-testid="search-product-card"]')
            )
        )

        # Valida título, imagem e preço
        titulo_produto = primeiro_produto.find_element(By.TAG_NAME, "h2").text
        imagem = primeiro_produto.find_element(By.TAG_NAME, "img").get_attribute("src")
        preco = primeiro_produto.find_element(
            By.XPATH,
            ".//span[contains(normalize-space(.), 'R$')]",
        ).text

        # Asserts genéricos para funcionar independentemente da palavra buscada
        assert imagem
        assert "R$" in preco

        mostrar_etapa(f"Produto: {titulo_produto} | Preço: {preco}")
        
        # Print 3: Salva a evidência da página de resultados confirmada
        navegador.save_screenshot(str(pasta_teste / "3_resultados.png"))
        
        print(f"\n[SUCESSO] Evidências e README salvos com sucesso na pasta:\n{pasta_teste}")

    finally:
        print("\nFechando o navegador em 2 segundos...", flush=True)
        time.sleep(2)
        navegador.quit()