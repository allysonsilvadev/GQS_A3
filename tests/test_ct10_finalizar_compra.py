# Projeto: Automação de Testes - Demoblaze (Avaliação A3)
# CT-10: Finalização de Compra (Place Order)

import re
import time
import unicodedata
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SITE = "https://www.demoblaze.com/"
PASTA_EVIDENCIAS = Path(__file__).resolve().parents[1] / "Evidencias"


def mostrar_etapa(mensagem):
    print(f"\n[CT-10] {mensagem}", flush=True)
    time.sleep(1.5)


def higienizar_nome_pasta(texto):
    """Remove acentos e caracteres especiais para gerar nomes de pastas seguros."""
    sem_acento = (
        unicodedata.normalize("NFKD", texto)
        .encode("ASCII", "ignore")
        .decode("ASCII")
    )
    limpo = re.sub(r"[^a-zA-Z0-9]+", "_", sem_acento).strip("_")
    return limpo.title() if limpo else "Comprador"


def criar_estrutura_evidencias(nome_produto, comprador, pais, cidade):
    """Cria a subpasta estruturada com data/hora e o README.txt exigido pela A3."""
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    comprador_limpo = higienizar_nome_pasta(comprador)

    # Cria o caminho: Evidencias/CT-10/Compra_Rodrigo_Conceicao_Data_Hora
    caminho_pasta = PASTA_EVIDENCIAS / "CT-10" / f"Compra_{comprador_limpo}_{data_hora}"
    caminho_pasta.mkdir(parents=True, exist_ok=True)

    caminho_readme = caminho_pasta / "README.txt"
    with open(caminho_readme, "w", encoding="utf-8") as f:
        f.write("Detalhes da Execucao - CT-10 (Finalizacao de Compra - Place Order)\n")
        f.write(f"Produto Comprado: {nome_produto}\n")
        f.write(f"Comprador: {comprador}\n")
        f.write(f"Localidade: {cidade} - {pais}\n")
        f.write(f"Data e Hora: {data_hora}\n")
        f.write("Status Inicial: Em execucao...\n")

    return caminho_pasta, caminho_readme


def atualizar_readme_sucesso(caminho_readme, titulo_modal, id_pedido, resumo_pedido):
    """Atualiza o README.txt com o ID exclusivo e o resumo da compra confirmada."""
    with open(caminho_readme, "a", encoding="utf-8") as f:
        f.write("Resultado Final: SUCESSO. Pedido finalizado e confirmado.\n")
        f.write(f"Titulo da Confirmacao: '{titulo_modal}'\n")
        f.write(f"ID do Pedido Gerado: {id_pedido}\n")
        f.write("Resumo Exibido no Modal:\n")
        for linha in resumo_pedido.splitlines():
            if linha.strip():
                f.write(f"  - {linha.strip()}\n")


def test_ct10_finalizar_compra(
    nome_produto="Samsung galaxy s6",
    comprador="Rodrigo Conceição",
    pais="Brasil",
    cidade="Curitiba",
    cartao="1234567812345678",
    mes="11",
    ano="2026",
):
    """
    Adiciona um produto ao carrinho no Demoblaze, acessa 'Cart', abre 'Place Order',
    preenche os dados de cobrança (com ou sem caracteres especiais), clica em 'Purchase'
    e valida o modal verde 'Thank you for your purchase!' com o ID do pedido.
    """
    pasta_teste, caminho_readme = criar_estrutura_evidencias(
        nome_produto, comprador, pais, cidade
    )

    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--window-size=1366,1000")
    navegador = webdriver.Chrome(options=opcoes)

    try:
        # 1. Acessa a página inicial e abre o produto escolhido
        navegador.get(SITE)
        WebDriverWait(navegador, 20).until(
            EC.visibility_of_element_located((By.ID, "tbodyid"))
        )
        mostrar_etapa("Página inicial do Demoblaze carregada.")

        link_produto = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[@id='tbodyid']//a[contains(normalize-space(.), '{nome_produto}')]")
            )
        )
        mostrar_etapa(f"Selecionando produto '{nome_produto}'...")
        link_produto.click()

        # 2. Adiciona o produto ao carrinho e aceita o alerta
        WebDriverWait(navegador, 15).until(EC.url_contains("prod.html"))
        botao_adicionar = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(normalize-space(.), 'Add to cart')]")
            )
        )
        botao_adicionar.click()

        alerta = WebDriverWait(navegador, 15).until(EC.alert_is_present())
        mostrar_etapa(f"Produto adicionado (alerta: '{alerta.text}'). Indo para o carrinho...")
        alerta.accept()

        # 3. Acessa o menu 'Cart' e confirma o item listado
        menu_carrinho = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable((By.ID, "cartur"))
        )
        menu_carrinho.click()

        WebDriverWait(navegador, 15).until(EC.url_contains("cart.html"))
        WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//tbody[@id='tbodyid']/tr[td[contains(normalize-space(.), '{nome_produto}')]]")
            )
        )

        # Print 1: Carrinho pronto para clicar em 'Place Order'
        time.sleep(1)
        navegador.save_screenshot(str(pasta_teste / "1_carrinho_com_produto.png"))

        # 4. Clica no botão 'Place Order' para abrir o modal de checkout
        botao_place_order = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@data-target='#orderModal' or contains(normalize-space(.), 'Place Order')]")
            )
        )
        mostrar_etapa("Abrindo modal de finalização de compra (Place Order)...")
        botao_place_order.click()

        # 5. Preenche todos os campos do formulário de compra
        campo_nome = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.ID, "name"))
        )
        campo_pais = navegador.find_element(By.ID, "country")
        campo_cidade = navegador.find_element(By.ID, "city")
        campo_cartao = navegador.find_element(By.ID, "card")
        campo_mes = navegador.find_element(By.ID, "month")
        campo_ano = navegador.find_element(By.ID, "year")

        for campo, valor in (
            (campo_nome, comprador),
            (campo_pais, pais),
            (campo_cidade, cidade),
            (campo_cartao, cartao),
            (campo_mes, mes),
            (campo_ano, ano),
        ):
            campo.clear()
            campo.send_keys(valor)

        mostrar_etapa(f"Formulário preenchido para '{comprador}' ({cidade} - {pais}).")

        # Print 2: Modal 'Place Order' preenchido antes de clicar em 'Purchase'
        time.sleep(1)
        navegador.save_screenshot(str(pasta_teste / "2_formulario_compra_preenchido.png"))

        # 6. Clica em 'Purchase' para concluir o pedido
        botao_purchase = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@id='orderModal']//button[contains(normalize-space(.), 'Purchase')]")
            )
        )
        mostrar_etapa("Clicando em 'Purchase' e aguardando confirmação do pedido...")
        botao_purchase.click()

        # 7. Aguarda o modal verde de confirmação (SweetAlert) e extrai os dados
        modal_sucesso = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.sweet-alert.visible"))
        )
        titulo_modal = modal_sucesso.find_element(By.TAG_NAME, "h2").text.strip()
        resumo_pedido = modal_sucesso.find_element(By.CSS_SELECTOR, "p.lead").text.strip()

        # Extrai o ID numérico exclusivo gerado pelo Demoblaze
        match_id = re.search(r"Id:\s*(\d+)", resumo_pedido)
        id_pedido = match_id.group(1) if match_id else ""

        # 8. Validações da compra concluída
        assert "thank you for your purchase" in titulo_modal.lower(), (
            f"Título de confirmação inesperado: '{titulo_modal}'"
        )
        assert id_pedido != "", (
            f"ID do pedido não encontrado no resumo: '{resumo_pedido}'"
        )
        assert comprador in resumo_pedido, (
            f"Nome do comprador '{comprador}' não apareceu no resumo do pedido."
        )
        assert cartao in resumo_pedido, (
            f"Número do cartão '{cartao}' não apareceu no resumo do pedido."
        )

        mostrar_etapa(f"Compra confirmada! Título: '{titulo_modal}' | ID do Pedido: {id_pedido}")

        # Print 3: Modal verde 'Thank you for your purchase!' com o ID do pedido visível
        time.sleep(1)
        navegador.save_screenshot(str(pasta_teste / "3_confirmacao_compra.png"))

        # 9. Fecha o modal de confirmação clicando em 'OK'
        botao_ok = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.sweet-alert button.confirm"))
        )
        botao_ok.click()

        atualizar_readme_sucesso(caminho_readme, titulo_modal, id_pedido, resumo_pedido)
        print(f"\n[SUCESSO] Evidências e README salvos na pasta:\n{pasta_teste}")

    finally:
        print("\nFechando o navegador em 2 segundos...", flush=True)
        time.sleep(2)
        navegador.quit()


if __name__ == "__main__":
    # Permite testar os dois cenários (sem e com caracteres especiais) diretamente
    test_ct10_finalizar_compra(
        nome_produto="Samsung galaxy s6",
        comprador="Rodrigo QA",
        pais="Brasil",
        cidade="Curitiba",
        cartao="1234567812345678",
        mes="11",
        ano="2026",
    )
    test_ct10_finalizar_compra(
        nome_produto="Samsung galaxy s6",
        comprador="Rodrigo Conceição",
        pais="Brasil",
        cidade="São Paulo",
        cartao="1234567812345678",
        mes="11",
        ano="2026",
    )