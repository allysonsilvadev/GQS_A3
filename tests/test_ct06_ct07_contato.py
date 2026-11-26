# Projeto: Automação de Testes - Demoblaze (Avaliação A3)
# CT-06 e CT-07: Formulário de Contato (Sem e Com Caracteres Especiais)

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


def mostrar_etapa(caso_teste, mensagem):
    print(f"\n[{caso_teste}] {mensagem}", flush=True)
    time.sleep(1.5)


def higienizar_nome_pasta(texto):
    """Remove acentos e caracteres especiais para gerar nomes de pastas seguros."""
    sem_acento = (
        unicodedata.normalize("NFKD", texto)
        .encode("ASCII", "ignore")
        .decode("ASCII")
    )
    limpo = re.sub(r"[^a-zA-Z0-9]+", "_", sem_acento).strip("_")
    return limpo.title() if limpo else "Execucao"


def criar_estrutura_evidencias(caso_teste, email, nome, mensagem):
    """Cria a subpasta estruturada com data/hora e o README.txt exigido pela A3."""
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_limpo = higienizar_nome_pasta(nome)

    # Cria o caminho: Evidencias/CT-06/Contato_Rodrigo_Qa_Data_Hora
    # ou Evidencias/CT-07/Contato_Joao_Conceicao_Data_Hora
    caminho_pasta = PASTA_EVIDENCIAS / caso_teste / f"Contato_{nome_limpo}_{data_hora}"
    caminho_pasta.mkdir(parents=True, exist_ok=True)

    caminho_readme = caminho_pasta / "README.txt"
    with open(caminho_readme, "w", encoding="utf-8") as f:
        f.write(f"Detalhes da Execucao - {caso_teste} (Formulario de Contato)\n")
        f.write(f"E-mail Informado: {email}\n")
        f.write(f"Nome Informado: {nome}\n")
        f.write(f"Mensagem Enviada: {mensagem}\n")
        f.write(f"Data e Hora: {data_hora}\n")
        f.write("Status Inicial: Em execucao...\n")

    return caminho_pasta, caminho_readme


def atualizar_readme_sucesso(caminho_readme, texto_alerta):
    """Atualiza o README.txt registrando a mensagem exata do alerta de confirmação."""
    with open(caminho_readme, "a", encoding="utf-8") as f:
        f.write("Resultado Final: SUCESSO. Formulario enviado e aceito pelo sistema.\n")
        f.write(f"Mensagem do Alerta Capturada: '{texto_alerta}'\n")


def test_enviar_formulario_contato(
    caso_teste="CT-06",
    email="qa.teste@exemplo.com",
    nome="Rodrigo QA",
    mensagem="Duvida sobre disponibilidade do Notebook Y e Celular X",
):
    """
    Acessa o menu 'Contact' no Demoblaze, preenche e-mail, nome e mensagem
    (suportando textos com e sem caracteres especiais), clica em 'Send message'
    e valida o alerta 'Thanks for the message!!'.
    """
    pasta_teste, caminho_readme = criar_estrutura_evidencias(
        caso_teste, email, nome, mensagem
    )

    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--window-size=1366,1000")
    navegador = webdriver.Chrome(options=opcoes)

    try:
        # 1. Acessa a página inicial e aguarda a vitrine carregar
        navegador.get(SITE)
        WebDriverWait(navegador, 20).until(
            EC.visibility_of_element_located((By.ID, "tbodyid"))
        )
        mostrar_etapa(caso_teste, "Página inicial do Demoblaze carregada.")

        # Print 1: Página inicial antes de abrir o modal de contato
        navegador.save_screenshot(str(pasta_teste / "1_pagina_inicial.png"))

        # 2. Clica no menu superior 'Contact' para abrir o modal
        menu_contato = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[@data-target='#exampleModal' or contains(normalize-space(.), 'Contact')]")
            )
        )
        mostrar_etapa(caso_teste, "Abrindo modal do formulário de contato...")
        menu_contato.click()

        # 3. Aguarda os campos do modal ficarem visíveis e preenche os parâmetros recebidos
        campo_email = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.ID, "recipient-email"))
        )
        campo_nome = navegador.find_element(By.ID, "recipient-name")
        campo_mensagem = navegador.find_element(By.ID, "message-text")

        campo_email.clear()
        campo_email.send_keys(email)

        campo_nome.clear()
        campo_nome.send_keys(nome)

        campo_mensagem.clear()
        campo_mensagem.send_keys(mensagem)

        mostrar_etapa(caso_teste, f"Formulário preenchido para '{nome}'.")

        # Print 2: Modal preenchido antes do envio (comprova a digitação com/sem caracteres especiais)
        time.sleep(1)
        navegador.save_screenshot(str(pasta_teste / "2_formulario_preenchido.png"))

        # 4. Clica em 'Send message' e aguarda o alerta de confirmação
        botao_enviar = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@id='exampleModal']//button[contains(normalize-space(.), 'Send message')]")
            )
        )
        mostrar_etapa(caso_teste, "Enviando mensagem e aguardando alerta de confirmação...")
        botao_enviar.click()

        alerta = WebDriverWait(navegador, 15).until(EC.alert_is_present())
        texto_alerta = alerta.text
        mostrar_etapa(caso_teste, f"Alerta capturado: '{texto_alerta}'")

        # 5. Valida a mensagem do alerta e confirma o pop-up
        assert "thanks for the message" in texto_alerta.lower(), (
            f"Mensagem inesperada no alerta: '{texto_alerta}'"
        )
        alerta.accept()

        # Print 3: Tela após confirmação do alerta e fechamento do modal
        time.sleep(1)
        navegador.save_screenshot(str(pasta_teste / "3_apos_envio_mensagem.png"))

        atualizar_readme_sucesso(caminho_readme, texto_alerta)
        print(f"\n[SUCESSO] Evidências e README salvos na pasta:\n{pasta_teste}")

    finally:
        print("\nFechando o navegador em 2 segundos...", flush=True)
        time.sleep(2)
        navegador.quit()


if __name__ == "__main__":
    # Permite testar CT-06 e CT-07 individualmente rodando este arquivo
    test_enviar_formulario_contato(
        caso_teste="CT-06",
        email="qa.teste@exemplo.com",
        nome="Rodrigo QA",
        mensagem="Duvida sobre disponibilidade do Notebook Y e Celular X",
    )
    test_enviar_formulario_contato(
        caso_teste="CT-07",
        email="qa.teste@exemplo.com",
        nome="João Conceição",
        mensagem="Solicitação de cotação e informações de manutenção do aparelho!",
    )