# Trabalho Acadêmico P2 - Laboratório de Programação Back-end

Esta é uma API REST para gerenciamento de dados de produtos, desenvolvida em **FastAPI**, persistindo dados em um banco de dados relacional **PostgreSQL** orquestrado através do **Docker Compose**. O projeto também inclui testes automatizados completos utilizando **Pytest** com isolamento de banco de dados.

---

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e de alta performance para Python.
- **PostgreSQL**: Banco de dados relacional robusto.
- **SQLAlchemy**: ORM para mapeamento objeto-relacional estruturado.
- **Pydantic v2**: Validação de esquemas e tipos de dados.
- **Docker & Docker Compose**: Containerização e orquestração de serviços.
- **Pytest**: Framework para testes automatizados.
- **SQLite**: Banco relacional leve utilizado em memória/arquivo temporário para execução dos testes de forma isolada.

---

## 📂 Estrutura do Projeto

```
trabalho p2/
├── .env                  # Variáveis de ambiente locais para Docker
├── .env.example          # Exemplo de configurações de variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo controle de versão Git
├── Dockerfile            # Instruções de montagem da imagem Docker da API
├── docker-compose.yml    # Orquestração do PostgreSQL e da API
├── requirements.txt      # Dependências da aplicação
├── app/
│   ├── __init__.py       # Marca o diretório app como pacote
│   ├── config.py         # Leitura de variáveis e configurações do Pydantic Settings
│   ├── database.py       # Criação do Engine, sessões e dependência do SQLAlchemy
│   ├── models.py         # Declaração do modelo ORM SQLAlchemy
│   ├── schemas.py        # Declaração dos Schemas de validação Pydantic
│   ├── crud.py           # Abstração de operações SQL (Queries e Inserções)
│   ├── main.py           # Ponto de entrada, lifespan e rotas da API
│   └── routers/
│       ├── __init__.py   # Marca o diretório routers como pacote
│       └── product.py    # Definição das rotas REST de CRUD para Produtos
└── tests/
    ├── __init__.py       # Marca o diretório tests como pacote
    ├── conftest.py       # Fixtures globais do pytest (cliente de testes e SQLite)
    └── test_product.py   # Suite de testes automatizados do CRUD
```

---

## 🚀 Como Executar a Aplicação com Docker Compose

Siga o passo a passo abaixo para construir a imagem da API e subir os serviços de banco de dados e aplicação:

### 1. Pré-requisitos
Certifique-se de possuir o **Docker** e o **Docker Compose** instalados em sua máquina.

### 2. Copiar arquivo de variáveis de ambiente
Copie o arquivo `.env.example` para `.env` (já criamos isso na pasta do projeto):
```bash
cp .env.example .env
```

### 3. Iniciar os containers
Execute o comando abaixo na pasta raiz do projeto para compilar a imagem e subir os serviços em segundo plano (`-d`):
```bash
docker compose up --build -d
```
O Docker Compose fará o seguinte:
1. Subirá um container PostgreSQL 15, configurará as credenciais e aguardará o banco de dados estar pronto (Healthcheck).
2. Compilará a imagem Python 3.11-slim da API e iniciará o servidor Uvicorn na porta `8000`.

### 4. Acessar a documentação interativa
Com os containers ativos, abra o navegador e acesse a documentação gerada automaticamente pelo FastAPI:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 5. Parar a execução
Para parar e remover os containers, mantendo a integridade dos dados salvos no volume:
```bash
docker compose down
```

---

## 🧪 Como Executar os Testes Automatizados

Os testes automatizados foram criados utilizando Pytest e validam todas as operações do CRUD do recurso `/produtos/`. Eles são 100% seguros e isolados, rodando em cima de uma base de dados SQLite local (`test.db`) configurada automaticamente antes da execução dos testes.

### Opção A: Executar Localmente (com Virtualenv)

Se você desejar rodar os testes localmente sem precisar rodar os containers Docker:

1. Acesse a pasta do projeto.
2. Ative o ambiente virtual (já configurado):
   ```bash
   source .venv/bin/activate
   ```
3. Execute o comando de testes:
   ```bash
   pytest -v
   ```

### Opção B: Executar dentro de um Container Temporário do Docker

Se você preferir executar os testes em um ambiente Docker isolado sem instalar nada na máquina local:

```bash
docker compose run --rm web pytest -v
```

### Opção C: Execução Automática via GitHub Actions (CI/CD)

O projeto está configurado com um pipeline de integração contínua (CI) no arquivo [.github/workflows/tests.yml](file:///.github/workflows/tests.yml). 

Toda vez que você enviar novos commits para o GitHub:
1. Os testes serão executados de forma totalmente automatizada em um container limpo.
2. O status da execução (sucesso/falha) será exibido diretamente na aba **Actions** do seu repositório GitHub e ao lado dos seus commits.

---

## 🐙 Como Enviar o Projeto para o GitHub

Caso ainda não tenha enviado o projeto para o seu repositório no GitHub, siga estes comandos no terminal local:

1. **Crie um repositório vazio no GitHub** (não adicione README, gitignore ou licença, pois o projeto já possui esses arquivos).
2. **Adicione o endereço remoto do repositório** criado (substitua `seu-usuario` e `nome-do-repositorio`):
   ```bash
   git remote add origin https://github.com/seu-usuario/nome-do-repositorio.git
   ```
3. **Adicione e comente as novas alterações** (incluindo o pipeline de testes):
   ```bash
   git add .
   git commit -m "feat: adiciona pipeline de CI do GitHub Actions"
   ```
4. **Envie os arquivos para o GitHub**:
   ```bash
   git branch -M main
   git push -u origin main
   ```

---

## 📌 Rotas da API REST

A API possui as seguintes rotas expostas no endpoint de produtos:

| Método | Rota | Descrição | Status Sucesso |
| :--- | :--- | :--- | :--- |
| **POST** | `/produtos/` | Cadastra um novo produto | `201 Created` |
| **GET** | `/produtos/` | Retorna lista paginada de produtos | `200 OK` |
| **GET** | `/produtos/{product_id}` | Obtém dados de um produto específico | `200 OK` |
| **PUT** | `/produtos/{product_id}` | Atualiza dados de um produto | `200 OK` |
| **DELETE** | `/produtos/{product_id}` | Exclui um produto do banco | `204 No Content` |
