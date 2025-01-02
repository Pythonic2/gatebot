# Use uma imagem base do Python
FROM python:3.11

# Configura o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto para o contêiner
COPY . .

# Comando para iniciar o script principal
CMD ["python", "main.py"]
