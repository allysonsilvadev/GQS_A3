# Grupo Los Bagres

**Integrante registrado:** Allyson da Silva Pereira — RA 942516484

# GQS A3 — Entrega 2

## Ideia do projeto

Este projeto está sendo desenvolvido para a entrega parcial da avaliação A3. O objetivo é explorar testes automatizados da busca de produtos no site público do [Carrefour Brasil](https://www.carrefour.com.br/), usando Python, Selenium e Pytest.

O sistema testado é a busca do e-commerce. Os cenários verificam uma pesquisa válida e uma pesquisa com erro de digitação. O escopo atual não inclui login, carrinho ou compra.

## Cenários atuais

- **CT-01 — Busca válida:** procura “Air Fryer” e confere se a página apresenta produtos com título, imagem e preço. Salva uma captura dos resultados.
- **CT-02 — Erro de digitação:** procura “Liquedificador”. O Carrefour deve informar que não encontrou produtos e sugerir a grafia “liquidificador”. Salva uma captura da resposta.

## Organização atual

```text
GQS A3 ENTREGA 2/
├── tests/
│   ├── test_ct01_busca_valida.py
│   └── test_ct02_erro_digitacao.py
├── evidencias/          # capturas geradas durante os testes
├── .venv/               # ambiente virtual local, não enviado ao GitHub
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
