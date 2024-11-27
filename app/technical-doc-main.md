
```markdown
# Documentation Technique - Gestionnaire d'Opportunités

# 1. Point d'Entrée de l'Application (main.py)
---

### Description Générale
Le fichier `main.py` est le point d'entrée principal de l'application. Il initialise et configure l'application FastAPI, met en place le logging, et gère les chemins d'accès aux différentes ressources.

### Configuration et Initialisation

#### Configuration du Logging
```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```
- Configure le système de logging au niveau INFO
- Crée un logger spécifique pour ce module

#### Initialisation FastAPI
```python
app = FastAPI(
    title="Gestionnaire d'Opportunités",
    description="API pour la gestion et l'analyse des opportunités commerciales"
)
```
- Crée l'instance principale de l'application
- Définit le titre et la description pour la documentation automatique Swagger

### Gestion des Chemins

#### Configuration des Chemins
```python
BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data_sources" / "gold"
```
- `BASE_PATH` : Chemin racine du projet
- `DATA_PATH` : Chemin vers les données de l'application

#### Vérification et Création des Répertoires
- Vérifie l'existence du répertoire de données
- Crée les répertoires manquants si nécessaire
- Configure les chemins pour les fichiers statiques et les templates

### Montage des Ressources Statiques
```python
app.mount("/static", StaticFiles(directory=str(STATIC_PATH)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_PATH))
```
- Monte les fichiers statiques (CSS, JS, etc.)
- Configure le moteur de templates Jinja2

### Routes Principales

#### Route Racine
```python
@app.get("/")
async def home(request: Request)
```
- Affiche la page d'accueil de l'application
- Utilise le template index.html

#### Route de Test
```python
@app.get("/test")
async def test()
```
- Route simple pour vérifier le fonctionnement de l'API

### Intégration des Sous-Routes
```python
app.include_router(opportunities.router, prefix="/opportunities", tags=["Opportunities"])
app.include_router(health.router, prefix="/health", tags=["Health"])
```
- Intègre les routes pour la gestion des opportunités
- Intègre les routes pour le health check

### Démarrage de l'Application
```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
- Configure le serveur ASGI Uvicorn
- Expose l'application sur toutes les interfaces (0.0.0.0) sur le port 8000
```

Ce fichier `main.py` est essentiel pour la configuration et le démarrage de l'application. Il définit les routes principales, monte les ressources statiques, et intègre les sous-routes pour les différentes fonctionnalités de l'application.