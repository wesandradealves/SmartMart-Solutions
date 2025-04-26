
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
venv\Scripts\activate     # Para Windows
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
- **POST** `/products` - Cria um novo produto.
- **PUT** `/products/{product_id}` - Atualiza um produto existente.
- **DELETE** `/products/{product_id}` - Deleta um produto.
- **POST** `/products/upload-csv` - Faz upload de um arquivo CSV para importar produtos.

### Categorias

- **GET** `/categories` - Lista todas as categorias.
- **POST** `/categories` - Cria uma nova categoria.
- **PUT** `/categories/{category_id}` - Atualiza uma categoria existente.
- **DELETE** `/categories/{category_id}` - Deleta uma categoria.

### Vendas

- **GET** `/sales` - Lista todas as vendas, incluindo o cálculo de lucro.
- **POST** `/sales` - Cria uma nova venda.
- **PUT** `/sales/{sale_id}` - Atualiza uma venda existente.
- **DELETE** `/sales/{sale_id}` - Deleta uma venda.

### Exportação de Dados

- **GET** `/export/products` - Exporta os produtos para um arquivo CSV.
- **GET** `/export/categories` - Exporta as categorias para um arquivo CSV.
- **GET** `/export/sales` - Exporta as vendas para um arquivo CSV.
- **GET** `/export/sales_with_profit` - Exporta as vendas com lucro para um arquivo CSV.

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
