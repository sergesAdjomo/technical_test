# Chemin: Dockerfile
FROM python:3.11-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Définir le répertoire de travail
WORKDIR /app

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier les requirements et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Créer les répertoires nécessaires avec les bonnes permissions
RUN mkdir -p data_sources/gold exports \
    && chmod 777 exports

# Copier le code source de l'application
COPY app ./app
COPY static ./static
COPY exports ./exports

# Dfinir la variable d'environnement PORT
ENV PORT 8080

# Exposer le port
EXPOSE 8080

# Commande pour démarrer l'application
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}