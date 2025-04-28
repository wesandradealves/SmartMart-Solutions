# SmartMart Backend API

API para gerenciamento interno de produtos, categorias e vendas da SmartMart Solutions.

- Frontend [https://github.com/wesandradealves/SmartMart-Solutions---Front](https://github.com/wesandradealves/SmartMart-Solutions---Front) 

- Backend [https://github.com/wesandradealves/SmartMart-Solutions](https://github.com/wesandradealves/SmartMart-Solutions) 

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
    - `skip`: Offset (padrão: 0).
    - `limit`: Número de itens por página (padrão: 10).
  - **Resposta:**
    ```json
    {
      "items": [
        {
          "name": "Dell XPS 15",
          "description": "15.6-inch touchscreen laptop with Intel i9 and 32GB RAM",
          "price": 1999.99,
          "category_id": 3,
          "brand": "Dell",
          "id": 7
        },
        {
          "name": "GE Profile Smart Microwave",
          "description": "1.7 cu. ft. convection microwave with scan-to-cook technology",
          "price": 349.99,
          "category_id": 4,
          "brand": "GE",
          "id": 11
        },
        {
          "name": "Google Pixel 6 Pro",
          "description": "6.7-inch LTPO OLED with Google Tensor processor and 50MP camera",
          "price": 899.99,
          "category_id": 5,
          "brand": "Google",
          "id": 15
        },
        {
          "name": "LG French Door Refrigerator",
          "description": "26.2 cu. ft. smart refrigerator with ice maker and door-in-door",
          "price": 2199.99,
          "category_id": 2,
          "brand": "LG",
          "id": 4
        },
        {
          "name": "LG OLED55C1",
          "description": "55-inch OLED 4K Smart TV with AI ThinQ and G-Sync compatibility",
          "price": 1499.99,
          "category_id": 1,
          "brand": "LG",
          "id": 2
        },
        {
          "name": "Lenovo ThinkPad X1",
          "description": "14-inch business laptop with Intel i7 and 16GB RAM",
          "price": 1699.99,
          "category_id": 3,
          "brand": "Lenovo",
          "id": 9
        },
        {
          "name": "MacBook Pro 16",
          "description": "16-inch laptop with M1 Pro chip and 16GB unified memory",
          "price": 2499.99,
          "category_id": 3,
          "brand": "Apple",
          "id": 8
        },
        {
          "name": "Panasonic Countertop Microwave",
          "description": "1.3 cu. ft. 1100W microwave with inverter technology",
          "price": 179.99,
          "category_id": 4,
          "brand": "Panasonic",
          "id": 10
        },
        {
          "name": "Samsung 65\" QLED TV",
          "description": "65-inch 4K Smart TV with HDR and quantum dot technology",
          "price": 1299.99,
          "category_id": 1,
          "brand": "Samsung",
          "id": 1
        },
        {
          "name": "Samsung Countertop Microwave",
          "description": "1.1 cu. ft. microwave with sensor cooking",
          "price": 159.99,
          "category_id": 4,
          "brand": "Samsung",
          "id": 12
        }
      ],
      "total": 16
    }
    ```

- **POST** `/products` - Cria um novo produto.
- **PUT** `/products/{product_id}` - Atualiza um produto existente.
- **DELETE** `/products/{product_id}` - Deleta um produto.
- **POST** `/products/upload-csv` - Faz upload de um arquivo CSV para importar produtos.

## Histórico de Preços

- **Endpoint**: `/price-history/{product_id}`
- **Método**: `GET`
- **Descrição**: Retorna o histórico de preços de um produto específico, com suporte a ordenação por data ou preço.
- **Parâmetros de Path**:
  - `product_id`: ID do produto para o qual o histórico de preços será recuperado.
- **Parâmetros de Query**:
  - `sort` (opcional): Ordena os resultados. Valores possíveis: `asc` (ascendente) ou `desc` (descendente). O padrão é `asc`.
  - `sort_by` (opcional): Campo para ordenar os resultados. Valores possíveis: `date` ou `price`. O padrão é `date`.
- **Resposta**:
  - **Status Code**: 200 OK
  - **Corpo**:
    ```json
    [
      {
        "price": 1999.99,
        "date": "2024-01-01T00:00:00"
      },
      {
        "price": 1799.99,
        "date": "2024-03-01T00:00:00"
      },
      {
        "price": 1699.99,
        "date": "2024-05-01T00:00:00"
      }
    ]
    ```
  - **Descrição**: Retorna uma lista do histórico de preços, ordenada conforme os parâmetros `sort` e `sort_by`. O histórico inclui o preço e a data da alteração do preço.

---

### Exemplos de chamadas

1. **Ordenação por data (padrão - ascendente)**:
   ```http
   GET /price-history/7?sort=asc&sort_by=date
  
---

## Atualizar Desconto de Categoria

- **Endpoint**: `/products/categories/{category_id}/discount`
- **Método**: `PUT`
- **Descrição**: Atualiza o desconto de uma categoria específica.
- **Parâmetros de Path**:
  - `category_id`: ID da categoria a ser atualizada.
- **Parâmetros de Corpo**:
  - `discount_percentage` (float): Novo valor de desconto para a categoria (ex: 10.5 para 10,5% de desconto).
- **Resposta**:
  - **Status Code**: 200 OK
  - **Corpo**:
    ```bash
      curl -X 'PUT' \
        'http://localhost:8000/products/categories/4/discount?discount_percentage=5.0' \
        -H 'accept: application/json'
    ```

    ```json
      {
        "message": "Desconto atualizado com sucesso",
        "discount_percentage": 5,
        "category_id": 4,
        "updated_products": [
          {
            "product_id": 10,
            "name": "Panasonic Countertop Microwave",
            "price": 112.85373,
            "category_id": 4
          },
          {
            "product_id": 11,
            "name": "GE Profile Smart Microwave",
            "price": 219.44373000000002,
            "category_id": 4
          },
          {
            "product_id": 12,
            "name": "Samsung Countertop Microwave",
            "price": 100.31373,
            "category_id": 4
          }
        ]
      }
    ```
  - **Descrição**: Retorna os dados da categoria atualizada com o novo valor de desconto.


### Categorias

- **GET** `/categories` - Lista todas as categorias.
  - **Query parameters:**
    - `sort_by`: Campo para ordenação (`id` ou `name`).
    - `sort_order`: Direção da ordenação (`asc` ou `desc`).
    - `skip`: Offset (padrão: 0).
    - `limit`: Número de itens por página (padrão: 10).
  - **Resposta:**
    ```json
      {
          "items": [
              {
                  "name": "Laptops",
                  "description": "Laptops de alto desempenho",
                  "discount_percentage": 0.0,
                  "id": 3
              },
              {
                  "name": "Micro-ondas",
                  "description": "Micro-ondas para cozinha inteligente",
                  "discount_percentage": 12.0,
                  "id": 4
              },
              {
                  "name": "Refrigeradores",
                  "description": "Refrigeradores de última geração",
                  "discount_percentage": 0.0,
                  "id": 2
              },
              {
                  "name": "Smartphones",
                  "description": "Smartphones com tecnologia avançada",
                  "discount_percentage": 0.0,
                  "id": 5
              },
              {
                  "name": "Televisores",
                  "description": "TVs de alta definição e tecnologia avançada",
                  "discount_percentage": 0.0,
                  "id": 1
              }
          ],
          "total": 5
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
- **Query Parameters**:
  - `days`: Número de dias para considerar o cálculo do lucro (padrão: 365).
  - `product_id`: ID do produto para filtrar as vendas (opcional).

- **Exemplo de chamada**:

  ```http
  GET /sales/profit/total?days=30&product_id=12
  ```

  ```json
    {
      "total_profit": 2750.846,
      "days": 30,
      "name": "Produto Exemplo",  
      "sales": [
        {
          "product_id": 12,
          "quantity": 13,
          "total_price": 2079.87,
          "date": "2025-09-08T00:00:00",
          "profit": 415.974
        },
        {
          "product_id": 12,
          "quantity": 15,
          "total_price": 2399.85,
          "date": "2025-03-15T00:00:00",
          "profit": 479.97
        },
        {
          "product_id": 12,
          "quantity": 18,
          "total_price": 2879.82,
          "date": "2025-11-22T00:00:00",
          "profit": 575.964
        },
        {
          "product_id": 12,
          "quantity": 22,
          "total_price": 3519.78,
          "date": "2025-06-10T00:00:00",
          "profit": 703.956
        }
      ]
    }

  ```

  ```http
  GET /sales/profit/total?days=365
  ```

  ```json
    {
      "total_profit": 151562.662,
      "sales": [
        {
          "product_id": 1,
          "quantity": 12,
          "total_price": 15599.88,
          "date": "2025-01-15T00:00:00",
          "profit": 3119.976
        },
        {
          "product_id": 1,
          "quantity": 8,
          "total_price": 10399.92,
          "date": "2025-03-22T00:00:00",
          "profit": 2079.984
        },
        {
          "product_id": 1,
          "quantity": 15,
          "total_price": 19499.85,
          "date": "2025-07-05T00:00:00",
          "profit": 3899.97
        },
        {
          "product_id": 1,
          "quantity": 10,
          "total_price": 12999.9,
          "date": "2025-10-18T00:00:00",
          "profit": 2599.98
        },
        {
          "product_id": 2,
          "quantity": 6,
          "total_price": 8999.94,
          "date": "2025-02-12T00:00:00",
          "profit": 1799.9880000000003
        },
        {
          "product_id": 2,
          "quantity": 11,
          "total_price": 16499.89,
          "date": "2025-05-30T00:00:00",
          "profit": 3299.978
        },
        {
          "product_id": 2,
          "quantity": 9,
          "total_price": 13499.91,
          "date": "2025-09-14T00:00:00",
          "profit": 2699.982
        },
        {
          "product_id": 2,
          "quantity": 7,
          "total_price": 10499.93,
          "date": "2025-12-01T00:00:00",
          "profit": 2099.9860000000003
        },
        {
          "product_id": 3,
          "quantity": 5,
          "total_price": 9499.95,
          "date": "2025-01-28T00:00:00",
          "profit": 1899.9900000000002
        },
        {
          "product_id": 3,
          "quantity": 8,
          "total_price": 15199.92,
          "date": "2025-04-10T00:00:00",
          "profit": 3039.9840000000004
        },
        {
          "product_id": 3,
          "quantity": 3,
          "total_price": 5699.97,
          "date": "2025-08-23T00:00:00",
          "profit": 1139.9940000000001
        },
        {
          "product_id": 3,
          "quantity": 6,
          "total_price": 11399.94,
          "date": "2025-11-15T00:00:00",
          "profit": 2279.9880000000003
        },
        {
          "product_id": 4,
          "quantity": 4,
          "total_price": 8799.96,
          "date": "2025-02-05T00:00:00",
          "profit": 1759.992
        },
        {
          "product_id": 4,
          "quantity": 7,
          "total_price": 15399.93,
          "date": "2025-06-18T00:00:00",
          "profit": 3079.9860000000003
        },
        {
          "product_id": 4,
          "quantity": 3,
          "total_price": 6599.97,
          "date": "2025-09-27T00:00:00",
          "profit": 1319.9940000000001
        },
        {
          "product_id": 4,
          "quantity": 5,
          "total_price": 10999.95,
          "date": "2025-12-10T00:00:00",
          "profit": 2199.9900000000002
        },
        {
          "product_id": 5,
          "quantity": 3,
          "total_price": 8399.97,
          "date": "2025-03-08T00:00:00",
          "profit": 1679.994
        },
        {
          "product_id": 5,
          "quantity": 6,
          "total_price": 16799.94,
          "date": "2025-05-22T00:00:00",
          "profit": 3359.988
        },
        {
          "product_id": 5,
          "quantity": 2,
          "total_price": 5599.98,
          "date": "2025-08-15T00:00:00",
          "profit": 1119.9959999999999
        },
        {
          "product_id": 5,
          "quantity": 4,
          "total_price": 11199.96,
          "date": "2025-11-30T00:00:00",
          "profit": 2239.9919999999997
        },
        {
          "product_id": 6,
          "quantity": 8,
          "total_price": 11999.92,
          "date": "2025-01-20T00:00:00",
          "profit": 2399.984
        },
        {
          "product_id": 6,
          "quantity": 5,
          "total_price": 7499.95,
          "date": "2025-04-15T00:00:00",
          "profit": 1499.99
        },
        {
          "product_id": 6,
          "quantity": 10,
          "total_price": 14999.9,
          "date": "2025-07-27T00:00:00",
          "profit": 2999.98
        },
        {
          "product_id": 6,
          "quantity": 6,
          "total_price": 8999.94,
          "date": "2025-10-05T00:00:00",
          "profit": 1799.9880000000003
        },
        {
          "product_id": 7,
          "quantity": 15,
          "total_price": 29999.85,
          "date": "2025-02-18T00:00:00",
          "profit": 5999.97
        },
        {
          "product_id": 7,
          "quantity": 8,
          "total_price": 15999.92,
          "date": "2025-05-12T00:00:00",
          "profit": 3199.9840000000004
        },
        {
          "product_id": 7,
          "quantity": 12,
          "total_price": 23999.88,
          "date": "2025-09-03T00:00:00",
          "profit": 4799.976000000001
        },
        {
          "product_id": 7,
          "quantity": 10,
          "total_price": 19999.9,
          "date": "2025-12-15T00:00:00",
          "profit": 3999.9800000000005
        },
        {
          "product_id": 8,
          "quantity": 6,
          "total_price": 14999.94,
          "date": "2025-03-01T00:00:00",
          "profit": 2999.9880000000003
        },
        {
          "product_id": 8,
          "quantity": 9,
          "total_price": 22499.91,
          "date": "2025-06-25T00:00:00",
          "profit": 4499.982
        },
        {
          "product_id": 8,
          "quantity": 4,
          "total_price": 9999.96,
          "date": "2025-10-12T00:00:00",
          "profit": 1999.992
        },
        {
          "product_id": 8,
          "quantity": 7,
          "total_price": 17499.93,
          "date": "2025-12-28T00:00:00",
          "profit": 3499.9860000000003
        },
        {
          "product_id": 9,
          "quantity": 10,
          "total_price": 16999.9,
          "date": "2025-01-10T00:00:00",
          "profit": 3399.9800000000005
        },
        {
          "product_id": 9,
          "quantity": 12,
          "total_price": 20399.88,
          "date": "2025-04-22T00:00:00",
          "profit": 4079.9760000000006
        },
        {
          "product_id": 9,
          "quantity": 8,
          "total_price": 13599.92,
          "date": "2025-08-09T00:00:00",
          "profit": 2719.9840000000004
        },
        {
          "product_id": 9,
          "quantity": 5,
          "total_price": 8499.95,
          "date": "2025-11-05T00:00:00",
          "profit": 1699.9900000000002
        },
        {
          "product_id": 10,
          "quantity": 20,
          "total_price": 3599.8,
          "date": "2025-02-28T00:00:00",
          "profit": 719.96
        },
        {
          "product_id": 10,
          "quantity": 15,
          "total_price": 2699.85,
          "date": "2025-05-17T00:00:00",
          "profit": 539.97
        },
        {
          "product_id": 10,
          "quantity": 25,
          "total_price": 4499.75,
          "date": "2025-09-20T00:00:00",
          "profit": 899.95
        },
        {
          "product_id": 10,
          "quantity": 18,
          "total_price": 3239.82,
          "date": "2025-12-03T00:00:00",
          "profit": 647.964
        },
        {
          "product_id": 11,
          "quantity": 8,
          "total_price": 2799.92,
          "date": "2025-01-25T00:00:00",
          "profit": 559.984
        },
        {
          "product_id": 11,
          "quantity": 12,
          "total_price": 4199.88,
          "date": "2025-04-30T00:00:00",
          "profit": 839.9760000000001
        },
        {
          "product_id": 11,
          "quantity": 6,
          "total_price": 2099.94,
          "date": "2025-07-15T00:00:00",
          "profit": 419.98800000000006
        },
        {
          "product_id": 11,
          "quantity": 10,
          "total_price": 3499.9,
          "date": "2025-10-28T00:00:00",
          "profit": 699.98
        },
        {
          "product_id": 12,
          "quantity": 15,
          "total_price": 2399.85,
          "date": "2025-03-15T00:00:00",
          "profit": 479.97
        },
        {
          "product_id": 12,
          "quantity": 22,
          "total_price": 3519.78,
          "date": "2025-06-10T00:00:00",
          "profit": 703.9560000000001
        },
        {
          "product_id": 12,
          "quantity": 13,
          "total_price": 2079.87,
          "date": "2025-09-08T00:00:00",
          "profit": 415.974
        },
        {
          "product_id": 12,
          "quantity": 18,
          "total_price": 2879.82,
          "date": "2025-11-22T00:00:00",
          "profit": 575.964
        },
        {
          "product_id": 13,
          "quantity": 25,
          "total_price": 27499.75,
          "date": "2025-02-08T00:00:00",
          "profit": 5499.950000000001
        },
        {
          "product_id": 13,
          "quantity": 30,
          "total_price": 32999.7,
          "date": "2025-05-25T00:00:00",
          "profit": 6599.94
        },
        {
          "product_id": 13,
          "quantity": 18,
          "total_price": 19799.82,
          "date": "2025-08-30T00:00:00",
          "profit": 3959.964
        },
        {
          "product_id": 13,
          "quantity": 22,
          "total_price": 24199.78,
          "date": "2025-12-20T00:00:00",
          "profit": 4839.956
        },
        {
          "product_id": 14,
          "quantity": 12,
          "total_price": 14399.88,
          "date": "2025-01-05T00:00:00",
          "profit": 2879.976
        },
        {
          "product_id": 14,
          "quantity": 15,
          "total_price": 17999.85,
          "date": "2025-04-18T00:00:00",
          "profit": 3599.97
        },
        {
          "product_id": 14,
          "quantity": 10,
          "total_price": 11999.9,
          "date": "2025-07-22T00:00:00",
          "profit": 2399.98
        },
        {
          "product_id": 14,
          "quantity": 8,
          "total_price": 9599.92,
          "date": "2025-10-15T00:00:00",
          "profit": 1919.9840000000002
        },
        {
          "product_id": 15,
          "quantity": 20,
          "total_price": 17999.8,
          "date": "2025-03-10T00:00:00",
          "profit": 3599.96
        },
        {
          "product_id": 15,
          "quantity": 15,
          "total_price": 13499.85,
          "date": "2025-06-22T00:00:00",
          "profit": 2699.9700000000003
        },
        {
          "product_id": 15,
          "quantity": 25,
          "total_price": 22499.75,
          "date": "2025-09-15T00:00:00",
          "profit": 4499.95
        },
        {
          "product_id": 15,
          "quantity": 18,
          "total_price": 16199.82,
          "date": "2025-12-05T00:00:00",
          "profit": 3239.964
        }
      ]
    }
  ```

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
    - `skip`: Offset (padrão: 0).
    - `limit`: Número de itens por página (padrão: 10).
  - **Resposta:**
    ```json
      {
        "items": [
          {
            "email": "admin@smartmart.com",
            "username": "admin",
            "role": "admin",
            "created_at": "2024-01-01T00:00:00",
            "id": 1,
            "hashed_password": "$2b$12$H/5ySs7X417HSZpUc5vvMOgiHM.9TEaXVz1uob78a.plI9DcHSOh6"
          },
          {
            "email": "user@smartmart.com",
            "username": "user",
            "role": "viewer",
            "created_at": "2024-01-02T00:00:00",
            "id": 2,
            "hashed_password": "$2b$12$n6BMpKpR6cjvhZO1toR1H.05E2ZWcrgCjiurGD6Oin1Wzh5QHkZv6"
          }
        ],
        "total": 2
      }
    ```

- **POST** `/users` - Cria um novo usuário.
- **PUT** `/users/{user_id}` - Atualiza um usuário existente.
- **DELETE** `/users/{user_id}` - Deleta um usuário.

### 🔒 Rotas Protegidas

Somente usuários com a role `admin` têm acesso ao menu de usuários e podem realizar as seguintes ações:

- Visualizar a lista de usuários.
- Alterar informações de outros usuários.
- Deletar usuários.

Essas restrições garantem maior segurança e controle sobre as operações administrativas.

### 🔗 Serviços de Admin

- [**Gerenciamento de Usuários** ⭐](#usuários)

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
