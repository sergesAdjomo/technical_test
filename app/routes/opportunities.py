# app/routes/opportunities.py
from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, List
import logging
from ..services.opportunity_service import OpportunityInfoService
from ..models.opportunity import OpportunityResponse

logger = logging.getLogger(__name__)
router = APIRouter()
service = OpportunityInfoService("data_sources/gold")

# Route de recherche avancée - DOIT ÊTRE AVANT la route par ID
@router.get("/search", response_model=List[OpportunityResponse])
async def search_opportunities(
    age_min: Optional[int] = Query(None, description="Âge minimum"),
    age_max: Optional[int] = Query(None, description="Âge maximum"),
    revenu_min: Optional[float] = Query(None, description="Revenu minimum mensuel"),
    banque: Optional[str] = Query(None, description="Banque principale"),
    limit: int = Query(10, ge=1, le=100, description="Nombre maximum de résultats")
):
    """Recherche des opportunités selon différents critères."""
    try:
        logger.info(f"Recherche avancée - Critères: age_min={age_min}, age_max={age_max}, revenu_min={revenu_min}, banque={banque}")
        results = service.search_opportunities(
            age_min=age_min,
            age_max=age_max,
            revenu_min=revenu_min,
            banque=banque,
            limit=limit
        )
        if not results:
            logger.info("Aucun résultat trouvé pour la recherche avancée")
        else:
            logger.info(f"Nombre de résultats trouvés: {len(results)}")
        return results
    except Exception as e:
        logger.error(f"Erreur lors de la recherche avancée: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Route pour récupérer une opportunité par ID - APRÈS la route de recherche
@router.get("/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(
    opportunity_id: str = Path(..., description="ID de l'opportunité"),
    include_propositions: bool = Query(False, description="Inclure les propositions associées")
):
    """Récupère les informations détaillées d'une opportunité."""
    try:
        logger.info(f"Récupération de l'opportunité: {opportunity_id}")
        info = service.get_info(opportunity_id, include_propositions)
        if not info['est_exploitable']:
            logger.warning(f"Opportunité non exploitable: {opportunity_id}")
        return info
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'opportunité: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))