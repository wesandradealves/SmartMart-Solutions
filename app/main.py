from fastapi import FastAPI
from app.routers import products, categories, sales, export, users, price_history
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "products",
        "description": "Operações relacionadas aos produtos",
    },
    {
        "name": "categories",
        "description": "Operações relacionadas às categorias",
    },
    {
        "name": "sales",
        "description": "Operações relacionadas às vendas",
    },
    {
        "name": "export",
        "description": "Operações relacionadas à exportação de dados",
    },
    {
        "name": "users",
        "description": "Operações relacionadas à autenticação e gerenciamento de usuários",
    },
    {
        "name": "price-history",
        "description": "Operações relacionadas à histórico de preços dos produtos",
    },
]

app = FastAPI(
    title="SmartMart API",
    description="API para gerenciamento interno de produtos, categorias e vendas da SmartMart Solutions.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(categories.router)
app.include_router(sales.router)
app.include_router(export.router)
app.include_router(users.router)
app.include_router(price_history.router)

