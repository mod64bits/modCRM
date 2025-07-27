# 1. Usar uma imagem base oficial do Python
FROM python:3.10-slim-buster

# 2. Definir variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Criar e definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# 4. Instalar as dependências
# Copia primeiro o requirements.txt para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar o restante do código do projeto para o diretório de trabalho
COPY . .

# A porta que o runserver vai expor dentro do contêiner
EXPOSE 9090