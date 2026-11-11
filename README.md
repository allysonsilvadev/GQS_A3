# Grupo Los Bagres

## Integrantes registrados:

 Allyson da Silva Pereira (RA: 942516484)
 
 Diogo Benedik de Oliveira (RA: 942519877)
 
 Rodrigo Cassol (RA: 942510010)
 
 Vinicius Gabriel Rodrigues Medrades (RA: 942618071)

# GQS A3 — Entrega 2

## Ideia do projeto

Este projeto está sendo desenvolvido para a entrega parcial da avaliação A3. O objetivo é explorar testes automatizados da busca de produtos no site público do [Demoblaze](https://www.demoblaze.com/), usando Python, Selenium e Pytest.

## Cenários atuais

- **CT-01: Navegação de Categorias (Laptops):** Acessar a página inicial, clicar na aba "Laptops" no menu lateral e validar se a vitrine atualiza para exibir apenas notebooks (ex: Sony vaio, MacBook).

- **CT-02: Visualização de Detalhes do Produto:** Clicar em um produto da vitrine inicial (ex: Samsung galaxy s6) e validar se a página de detalhes é carregada com sucesso, exibindo a imagem, o título do produto, o preço e o botão de compra.

- **CT-03: Adicionar Produto ao Carrinho:** 

- **CT-04: Validação de Itens no Carrinho:** Após adicionar um item, acessar o menu superior "Cart" e validar se o produto aparece na tabela de compras com o título e o preço correspondentes ao item escolhido.

- **CT-05: Exclusão de Produto do Carrinho:** Dentro do menu "Cart", clicar no botão "Delete" ao lado de um produto recém-adicionado e validar se a tabela é limpa e se o valor total da compra é atualizado.

- **CT-06: Formulário de Contato (Sem Caracteres Especiais):** Acessar o menu "Contact", preencher o formulário informando e-mail, nome e uma mensagem simples sem pontuações ou acentos (ex: testando com a palavra "geladeira"). Clicar em "Send message" e validar o alerta "Thanks for the message!!".

- **CT-07: Formulário de Contato (Com Caracteres Especiais):** Acessar o menu "Contact" e preencher o formulário utilizando uma mensagem com acentuação e cedilha (ex: testando com "coração de galinha"). Validar se o sistema suporta o envio e retorna o alerta de sucesso.

- **CT-08: Cadastro de Usuário (Sign up) Bloqueado:** Acessar o menu "Sign up", tentar registrar um nome de usuário que sabidamente já existe no banco de dados da loja e validar se o sistema barra a criação exibindo o alerta "This user already exist.".

- **CT-09: Login com Credenciais Incorretas** Acessar o menu "Log in", preencher um usuário ou senha inválidos e tentar entrar. Validar se o sistema rejeita o acesso exibindo o alerta "Wrong password." ou "User does not exist.".

- **CT-10: Finalização de Compra (Place Order)** Com um produto no carrinho, clicar no botão "Place Order". Preencher o formulário de endereço e cartão de crédito (testando a inserção de dados com e sem caracteres especiais) e clicar em "Purchase". Validar se o modal verde de confirmação "Thank you for your purchase!" é gerado contendo o ID exclusivo do pedido.

## Organização atual

```text
GQS A3 ENTREGA 2/
├── tests/
│   ├── __init__.py              # Transforma a pasta em módulo para os imports
│   ├── test_ct01_busca_valida.py
│   └── test_ct02_erro_digitacao.py
├── Evidencias/                  # Pasta gerada dinamicamente pela automação (ignorada no Git)
│   ├── CT-01/
│   │   ├── CelularX_2026-10-28_20-55-10/
│   │   │   ├── README.txt
│   │   │   ├── 1_pagina_inicial.png
│   │   │   ├── 2_termo_digitado.png
│   │   │   └── 3_resultados.png
│   │   └── NotebookY_2026-10-28_20-55-45/
│   │       ├── README.txt
│   │       └── ...
│   └── CT-02/
│       └── ...
├── .venv/                       # Ambiente virtual Python (ignorado no Git)
├── main.py                      # Programa centralizador que executa os testes
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

Esta organização é uma proposta de trabalho para a fase atual de testes e planejamento. **Ainda não é o padrão definitivo do projeto.** A estrutura poderá mudar conforme o grupo avaliar os cenários e decidir como organizar melhor os próximos testes.

## Dependências em avaliação

O `requirements.txt` registra as dependências do ambiente virtual atual, geradas com `pip freeze`. Nesta etapa estamos reutilizando as dependências da atividade anterior:

- **Pytest:** encontra e executa os cenários e apresenta o resultado das validações.
- **Selenium:** controla o Chrome e interage com a busca do site.
- **Pillow:** mantido por enquanto por compatibilidade com a atividade anterior; os dois cenários atuais não o utilizam diretamente.

A lista e as versões são **experimentais**. O grupo ainda está analisando as dependências necessárias; elas poderão ser atualizadas, removidas ou substituídas durante o desenvolvimento.

## Preparar o ambiente (PowerShell)

Na pasta do projeto, crie e ative o ambiente virtual e instale as dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Para atualizar `requirements.txt` com o estado atual do ambiente:

```powershell
python -m pip freeze > requirements.txt
```

## Executar os testes

Com `.venv` ativo, execute os dois cenários:

```powershell
python -m pytest -v -s
```

O Chrome fica visível para acompanhar as etapas. As capturas são salvas automaticamente em `evidencias/`.
