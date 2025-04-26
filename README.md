
# SmartMart Backend API

API para gerenciamento interno de produtos, categorias e vendas da SmartMart Solutions.

## Tecnologias

- **FastAPI** para construção da API.
- **SQLAlchemy** para ORM (Object Relational Mapper).
- **SQLite** como banco de dados local.
- **Pydantic** para validação de dados.
- **Pandas** para importar/exportar dados de/para CSV.

## Pré-requisitos

- **Docker** (opcional) - para rodar o backend em um container.
- **Python 3.11** ou superior.
- **pip** para instalação de dependências.
- **Passlib** e **bcrypt** para segurança de senhas.

```bash
pip install passlib[bcrypt]
```

## Instalação

### 1. Clonando o repositório

```bash
git clone https://github.com/seu-usuario/smartmart-backend-v4.git
cd smartmart-backend-v4
```

### 2. Criando o ambiente virtual

É recomendado criar um ambiente virtual para evitar conflitos de dependências:

```bash
python -m venv venv
source venv/bin/activate  # Para Linux/macOS
venv\Scripts\activate   # Para Windows
```

### 3. Instalando dependências

Instale as dependências com o pip:

```bash
pip install -r requirements.txt
```

## Rodando o Ambiente

### 1. Iniciando o banco de dados

Antes de rodar a aplicação, é necessário criar as tabelas no banco de dados e popular com dados iniciais.

#### Usando o Docker

Você pode rodar o backend utilizando Docker. Para isso, execute:

```bash
docker-compose up --build
```

O Docker irá levantar o container com o backend e as variáveis necessárias.

#### Usando diretamente o Python

Caso não esteja utilizando Docker, execute:

```bash
python populate_initial_data.py
```

Isso criará as tabelas no banco SQLite e irá popular as tabelas com dados iniciais (categorias, produtos, vendas).

### 2. Rodando a API

Com o banco de dados configurado, rode a aplicação FastAPI com o Uvicorn:

```bash
uvicorn app.main:app --reload
```

A aplicação estará disponível em [http://localhost:8000](http://localhost:8000).

## Endpoints

A API possui os seguintes endpoints principais:

### Produtos

- **GET** `/products` - Lista todos os produtos.
  - **Query parameters:**
    - `category_id`: Filtra os produtos pela categoria.
    - `title`: Filtra os produtos pelo título (nome).
    - `sort`: Ordena os resultados. Valores: `asc` ou `desc`.
    - `sort_by`: Escolhe o campo para ordenar. Valores: `name`, `category_id`, `brand`, `price`.
    - `page`: Número da página (padrão: 1).
    - `page_size`: Número de itens por página (padrão: 10).
  - **Resposta:**
    ```json
    {
      "total": 50,
      "page": 1,
      "page_size": 10,
      "items": [...]
    }
    ```

- **POST** `/products` - Cria um novo produto.
- **PUT** `/products/{product_id}` - Atualiza um produto existente.
- **DELETE** `/products/{product_id}` - Deleta um produto.
- **POST** `/products/upload-csv` - Faz upload de um arquivo CSV para importar produtos.

### Categorias

- **GET** `/categories` - Lista todas as categorias.
  - **Query parameters:**
    - `sort_by`: Campo para ordenação (`id` ou `name`).
    - `sort_order`: Direção da ordenação (`asc` ou `desc`).
    - `page`: Número da página (padrão: 1).
    - `page_size`: Número de itens por página (padrão: 10).
  - **Resposta:**
    ```json
    {
      "total": 10,
      "page": 1,
      "page_size": 10,
      "items": [...]
    }
    ```

- **POST** `/categories` - Cria uma nova categoria.
- **PUT** `/categories/{category_id}` - Atualiza uma categoria existente.
- **DELETE** `/categories/{category_id}` - Deleta uma categoria.

### Vendas

- **GET** `/sales` - Lista todas as vendas, incluindo o cálculo de lucro.
  - **Query parameters:**
    - `sort_by`: `"total_price"` ou `"profit"` ou `"date"` (padrão: `"total_price"`)
    - `sort_order`: `"asc"` ou `"desc"` (padrão: `"asc"`)
    - `days`: Número de dias retroativos para filtrar as vendas (padrão: `365` dias)
    - `skip`: Número de registros para pular (paginação)
    - `limit`: Quantidade máxima de registros para retornar
  - **Resposta:**
  - GET /sales?sort_by=profit&sort_order=desc&days=30&skip=0&limit=10
    ```json
    {
      "items": [
        {
          "id": 1,
          "product_id": 2,
          "quantity": 5,
          "total_price": 500.0,
          "date": "2024-04-25T00:00:00",
          "profit": 100.0
        }
      ],
      "total": 23
    }
    ```

- **POST** `/sales` - Cria uma nova venda.
- **PUT** `/sales/{sale_id}` - Atualiza uma venda existente.
- **DELETE** `/sales/{sale_id}` - Deleta uma venda.

### **Serviço de cálculo de lucro total**:
- **Endpoint**: `/sales/profit/total`
- **Método**: `GET`
- **Query Parameter**:
  - `days`: Número de dias para considerar o cálculo do lucro (padrão: 365).

### Exportação de Dados

- **GET** `/export/products` - Exporta os produtos para um arquivo CSV.
- **GET** `/export/categories` - Exporta as categorias para um arquivo CSV.
- **GET** `/export/sales` - Exporta as vendas para um arquivo CSV.
- **GET** `/export/sales_with_profit` - Exporta as vendas com lucro para um arquivo CSV.

### Usuários

- **GET** `/users` - Lista todos os usuários, com suporte a paginação e ordenação.
  - **Query parameters:**
    - `sort`: Ordena os resultados. Valores: `asc` ou `desc`.
    - `sort_by`: Campo para ordenar. Valores: `username`, `email`, `role`, `created_at`.
    - `page`: Número da página (padrão: 0).
    - `limit`: Número de itens por página (padrão: 10).
  - **Resposta:**
    ```json
    {
      "total": 5,
      "page": 1,
      "page_size": 10,
      "items": [
        {
          "id": 1,
          "email": "email@domain.com",
          "username": "admin",
          "role": "admin",
          "created_at": "2025-04-26T14:42:25.154Z"
        }
      ]
    }
    ```

- **POST** `/users` - Cria um novo usuário.
- **PUT** `/users/{user_id}` - Atualiza um usuário existente.
- **DELETE** `/users/{user_id}` - Deleta um usuário.

## 🔐 Autenticação

- POST /users/login: Envia username ou email + password, recebe token de sessão.
- POST /users/logout: Termina a sessão.
- O token é armazenado como cookie session_token (HTTP-only) para segurança.

## 🛡️ Segurança

- Senhas são armazenadas de forma segura usando bcrypt.
- Tokens de sessão são gerados com itsdangerous e têm tempo de expiração (1h).

## Estrutura de Arquivos

```plaintext
smartmart-backend-v4/
│
├── app/
│   ├── main.py                # Ponto de entrada da API
│   ├── models/                # Definições do banco de dados
│   ├── routers/               # Definições dos endpoints
│   ├── services/              # Lógicas auxiliares (ex: importação de CSV)
│   ├── schemas/               # Modelos de dados
│   └── database.py            # Conexão com o banco de dados
│
├── data/                      # Dados para popular o banco (CSV)
├── Dockerfile                 # Arquivo para criar a imagem do Docker
├── docker-compose.yml         # Configuração do Docker Compose
├── requirements.txt           # Dependências do projeto
└── populate_initial_data.py   # Script para popular o banco de dados
```

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
