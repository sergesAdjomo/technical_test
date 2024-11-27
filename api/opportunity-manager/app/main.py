# app/main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path 
import logging
from .services.opportunity_service import OpportunityInfoService
from .routes import opportunities, health
 
# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Créer l'application FastAPI  
app = FastAPI(
    title="Gestionnaire d'Opportunités",
    description="API pour la gestion et l'analyse des opportunités commerciales"
)

# Obtenir le chemin absolu du projet
BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data_sources" / "gold"

# Log des chemins pour debug
logger.info(f"Base path: {BASE_PATH}")
logger.info(f"Data path: {DATA_PATH}")

# Vérifier que le dossier de données existe
if not DATA_PATH.exists():
    logger.error(f"Data directory not found: {DATA_PATH}")
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    logger.info("Created data directory")

# Configurer les fichiers statiques et les templates
STATIC_PATH = BASE_PATH / "static"
TEMPLATES_PATH = BASE_PATH / "app" / "templates"

# Vérifier que les dossiers existent
if not STATIC_PATH.exists():
    logger.error(f"Static directory not found: {STATIC_PATH}")
if not TEMPLATES_PATH.exists():
    logger.error(f"Templates directory not found: {TEMPLATES_PATH}")

# Monter les fichiers statiques
app.mount("/static", StaticFiles(directory=str(STATIC_PATH)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_PATH))

# Initialiser le service
service = OpportunityInfoService(str(DATA_PATH))

# Inclure les routes
app.include_router(opportunities.router, prefix="/opportunities", tags=["Opportunities"])
app.include_router(health.router, prefix="/health", tags=["Health"])

@app.get("/")
async def home(request: Request):
    """
    Route principale qui affiche l'interface utilisateur
    """
    logger.info("Accessing home page")
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        logger.error(f"Error rendering template: {str(e)}")
        raise

@app.get("/test")
async def test():
    """
    Route de test simple
    """
    return {"message": "Test successful"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)