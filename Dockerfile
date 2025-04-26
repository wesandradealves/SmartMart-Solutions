FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "python -c 'from app.database import Base, engine; Base.metadata.create_all(bind=engine)' && python /app/populate_initial_data.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
