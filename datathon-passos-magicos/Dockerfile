FROM python:3.11-slim

WORKDIR /app

# Copia dependências primeiro (melhora cache do build)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto
COPY app ./app
COPY src ./src

# (Opcional) Copiar outros arquivos úteis
COPY README.md ./README.md

# Porta padrão do container
EXPOSE 8000

# Inicia a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
