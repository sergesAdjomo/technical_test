# Chemin: start.sh
#!/bin/bash

# Arrêter les conteneurs existants
echo "Arrêt des conteneurs existants..."
docker-compose down

# Construire/mettre à jour l'image
echo "Construction/Mise à jour de l'image..."
docker-compose build

# Démarrer l'application
echo "Démarrage de l'application..."
docker-compose up -d

# Attendre que l'application démarre
echo "Attente du démarrage de l'application..."
sleep 5

# Vérifier si l'application est en cours d'exécution
if docker-compose ps | grep -q "running"; then
    echo "Application démarrée ! Allez sur http://127.0.0.1:8000"
else
    echo "Erreur : l'application n'a pas démarré correctement."
    docker-compose logs
fi