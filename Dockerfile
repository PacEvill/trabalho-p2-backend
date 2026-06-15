FROM python:3.11-slim

WORKDIR /workspace

# Otimizações de ambiente para o contêiner
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalação das dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Cópia do código-fonte do projeto
COPY . .

EXPOSE 8000

# Comando para iniciar o servidor ASGI uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
