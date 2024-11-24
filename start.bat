:: Chemin: start.bat
@echo off
echo Arrêt des conteneurs existants...
docker-compose down

echo Construction/Mise à jour de l'image...
docker-compose build

echo Démarrage de l'application...
docker-compose up -d

echo Attente du démarrage de l'application...
timeout /t 5 /nobreak

echo.
docker-compose ps
echo.

:: Vérifier si l'application est en cours d'exécution
docker-compose ps | findstr "running" > nul
if %errorlevel% equ 0 (
    echo Application démarrée ! Allez sur http://127.0.0.1:8000
) else (
    echo Erreur : l'application n'a pas démarré correctement.
    docker-compose logs
)

echo Pour arrêter l'application, appuyez sur une touche
pause