# app/routes/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Vérifier l'état de l'API")
async def health_check():
    """
    Endpoint de healthcheck pour vérifier si l'API est fonctionnelle.
    
    Returns:
        dict: Statut de l'API et version
    """
    return {
        "status": "healthy",
        "version": "1.0.0"
    }