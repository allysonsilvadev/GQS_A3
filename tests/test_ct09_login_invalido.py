# Projeto: Automação de Testes - Demoblaze (Avaliação A3)
# CT-09: Login com Credenciais Incorretas

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
    print(f"\n[CT-09] {mensagem}", flush=True)
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

    # Cria o caminho: Evidencias/CT-09/Login_Usuario_Inexistente_Qa_Data_Hora
    caminho_pasta = PASTA_EVIDENCIAS / "CT-09" / f"Login_{usuario_limpo}_{data_hora}"
    caminho_pasta.mkdir(parents=True, exist_ok=True)

    caminho_readme = caminho_pasta / "README.txt"
    with open(caminho_readme, "w", encoding="utf-8") as f:
        f.write("Detalhes da Execucao - CT-09 (Login com Credenciais Incorretas)\n")
        f.write(f"Usuario Testado: {usuario}\n")
        f.write(f"Data e Hora: {data_hora}\n")
        f.write("Status Inicial: Em execucao...\n")

    return caminho_pasta, caminho_readme


def atualizar_readme_sucesso(caminho_readme, texto_alerta):
    """Atualiza o README.txt confirmando que o acesso com dados inválidos foi rejeitado."""
    with open(caminho_readme, "a", encoding="utf-8") as f:
        f.write("Resultado Final: SUCESSO. Acesso rejeitado corretamente pelo sistema.\n")
        f.write(f"Mensagem do Alerta Capturada: '{texto_alerta}'\n")


def test_ct09_login_credenciais_invalidas(usuario="usuario_inexistente_qa", senha="000"):
    """
    Acessa o menu 'Log in' no Demoblaze, informa usuário ou senha inválidos
    e valida se o alerta exibe 'Wrong password.' ou 'User does not exist.'.
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

        # Print 1: Página inicial antes de abrir o modal de login
        navegador.save_screenshot(str(pasta_teste / "1_pagina_inicial.png"))

        # 2. Clica no menu superior 'Log in' para abrir o modal
        menu_login = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable((By.ID, "login2"))
        )
        mostrar_etapa("Abrindo modal de login (Log in)...")
        menu_login.click()

        # 3. Aguarda os campos do modal ficarem visíveis e preenche usuário e senha
        campo_usuario = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.ID, "loginusername"))
        )
        campo_senha = navegador.find_element(By.ID, "loginpassword")

        campo_usuario.clear()
        campo_usuario.send_keys(usuario)

        campo_senha.clear()
        campo_senha.send_keys(senha)

        mostrar_etapa(f"Credenciais inválidas preenchidas para o usuário '{usuario}'.")

        # Print 2: Modal de login preenchido antes do clique
        time.sleep(1)
        navegador.save_screenshot(str(pasta_teste / "2_modal_login_preenchido.png"))

        # 4. Clica no botão 'Log in' dentro do modal e aguarda o alerta de rejeição
        botao_entrar = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@id='logInModal']//button[contains(normalize-space(.), 'Log in')]")
            )
        )
        mostrar_etapa("Clicando em 'Log in' e aguardando alerta de erro...")
        botao_entrar.click()

        alerta = WebDriverWait(navegador, 15).until(EC.alert_is_present())
        texto_alerta = alerta.text
        mostrar_etapa(f"Alerta capturado: '{texto_alerta}'")

        # 5. Valida se o alerta corresponde a usuário inexistente ou senha incorreta
        mensagens_esperadas = ("wrong password", "user does not exist")
        assert any(msg in texto_alerta.lower() for msg in mensagens_esperadas), (
            f"Mensagem inesperada no alerta: '{texto_alerta}'"
        )
        alerta.accept()

        # Print 3: Tela após confirmar o alerta (modal permanece aberto e usuário não entra)
        time.sleep(1)
        navegador.save_screenshot(str(pasta_teste / "3_apos_alerta_rejeicao.png"))

        atualizar_readme_sucesso(caminho_readme, texto_alerta)
        print(f"\n[SUCESSO] Evidências e README salvos na pasta:\n{pasta_teste}")

    finally:
        print("\nFechando o navegador em 2 segundos...", flush=True)
        time.sleep(2)
        navegador.quit()


if __name__ == "__main__":
    # Permite testar este arquivo individualmente (usuário inexistente ou senha errada)
    test_ct09_login_credenciais_invalidas("usuario_inexistente_qa", "000")