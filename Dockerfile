FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia todos os arquivos para dentro do container
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta
EXPOSE 8000

# Comando padrão para rodar o FastAPI
CMD ["sh", "-c", "python -c 'from app.database import Base, engine; Base.metadata.create_all(bind=engine)' && python /app/populate_initial_data.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
