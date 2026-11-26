# Projeto: Automação de Testes - Demoblaze (Avaliação A3)
# CT-08: Cadastro de Usuário (Sign up) Bloqueado

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
    print(f"\n[CT-08] {mensagem}", flush=True)
    time.sleep(1.5)


def higienizar_nome_pasta(texto):
    """Remove acentos e caracteres especiais para gerar nomes de pastas seguros."""
    sem_acento = (
        unicodedata.normalize("NFKD", texto)
        .encode("ASCII", "ignore")
        .decode("ASCII")
    )
    limpo = re.sub(r"[^a-zA-Z0-9]+", "_", sem_acento).strip("_")
    return limpo.title() if limpo else "Usuario"


def criar_estrutura_evidencias(usuario):
    """Cria a subpasta estruturada com data/hora e o README.txt exigido pela A3."""
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    usuario_limpo = higienizar_nome_pasta(usuario)

    # Cria o caminho: Evidencias/CT-08/Cadastro_Admin_Data_Hora
    caminho_pasta = PASTA_EVIDENCIAS / "CT-08" / f"Cadastro_{usuario_limpo}_{data_hora}"
    caminho_pasta.mkdir(parents=True, exist_ok=True)

    caminho_readme = caminho_pasta / "README.txt"
    with open(caminho_readme, "w", encoding="utf-8") as f:
        f.write("Detalhes da Execucao - CT-08 (Cadastro de Usuario Ja Existente)\n")
        f.write(f"Usuario Testado: {usuario}\n")
        f.write(f"Data e Hora: {data_hora}\n")
        f.write("Status Inicial: Em execucao...\n")

    return caminho_pasta, caminho_readme


def atualizar_readme_sucesso(caminho_readme, texto_alerta):
    """Atualiza o README.txt confirmando que o cadastro duplicado foi bloqueado."""
    with open(caminho_readme, "a", encoding="utf-8") as f:
        f.write("Resultado Final: SUCESSO. Sistema bloqueou o cadastro de usuario duplicado.\n")
        f.write(f"Mensagem do Alerta Capturada: '{texto_alerta}'\n")


def test_ct08_cadastro_usuario_existente(usuario="admin", senha="123"):
    """
    Acessa o menu 'Sign up' no Demoblaze, tenta cadastrar um usuário já existente
    no banco de dados da loja e valida o alerta 'This user already exist.'.
    """
    pasta_teste, caminho_readme = criar_estrutura_evidencias(usuario)

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

        # Print 1: Página inicial antes de abrir o modal de cadastro
        navegador.save_screenshot(str(pasta_teste / "1_pagina_inicial.png"))

        # 2. Clica no menu superior 'Sign up' para abrir o modal
        menu_signup = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable((By.ID, "signin2"))
        )
        mostrar_etapa("Abrindo modal de cadastro (Sign up)...")
        menu_signup.click()

        # 3. Aguarda os campos do modal ficarem visíveis e preenche usuário e senha
        campo_usuario = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.ID, "sign-username"))
        )
        campo_senha = navegador.find_element(By.ID, "sign-password")

        campo_usuario.clear()
        campo_usuario.send_keys(usuario)

        campo_senha.clear()
        campo_senha.send_keys(senha)

        mostrar_etapa(f"Dados preenchidos para tentativa de cadastro do usuário '{usuario}'.")

        # Print 2: Modal de Sign up preenchido antes do clique
        time.sleep(1)
        navegador.save_screenshot(str(pasta_teste / "2_modal_signup_preenchido.png"))

        # 4. Clica no botão 'Sign up' dentro do modal e aguarda o alerta de bloqueio
        botao_cadastrar = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@id='signInModal']//button[contains(normalize-space(.), 'Sign up')]")
            )
        )
        mostrar_etapa("Clicando em 'Sign up' e aguardando alerta de validação...")
        botao_cadastrar.click()

        alerta = WebDriverWait(navegador, 15).until(EC.alert_is_present())
        texto_alerta = alerta.text
        mostrar_etapa(f"Alerta capturado: '{texto_alerta}'")

        # 5. Valida a mensagem de bloqueio e aceita o alerta
        assert "this user already exist" in texto_alerta.lower(), (
            f"Mensagem inesperada no alerta: '{texto_alerta}'"
        )
        alerta.accept()

        # Print 3: Tela após confirmar o alerta (modal permanece aberto, impedindo o cadastro)
        time.sleep(1)
        navegador.save_screenshot(str(pasta_teste / "3_apos_alerta_bloqueio.png"))

        atualizar_readme_sucesso(caminho_readme, texto_alerta)
        print(f"\n[SUCESSO] Evidências e README salvos na pasta:\n{pasta_teste}")

    finally:
        print("\nFechando o navegador em 2 segundos...", flush=True)
        time.sleep(2)
        navegador.quit()


if __name__ == "__main__":
    # Permite testar este arquivo individualmente se desejar
    test_ct08_cadastro_usuario_existente("admin", "123")