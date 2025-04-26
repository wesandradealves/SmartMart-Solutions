from fastapi import FastAPI
from app.routers import products, categories, sales, export
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