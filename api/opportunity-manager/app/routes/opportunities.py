# app/routes/opportunities.py
from fastapi import APIRouter, HTTPException, Query, Path
from fastapi.responses import FileResponse  # Nouvel import
from typing import Optional, List
import logging
from pathlib import Path as PathLib  # Renommé pour éviter la confusion avec fastapi.Path
from ..services.opportunity_service import OpportunityInfoService
from ..models.opportunity import OpportunityResponse

logger = logging.getLogger(__name__)
router = APIRouter()
service = OpportunityInfoService()

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
            age_min,
            age_max,
            revenu_min,
            banque,
            limit
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
        print(info)
        print(info['est_exploitable'])
        if info['est_exploitable'] == "False":
            logger.warning(f"Opportunité non exploitable: {opportunity_id}")
        return info
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'opportunité: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Nouvelle route pour l'export
@router.get("/{opportunity_id}/export")
async def export_opportunity(opportunity_id: str):
    """Export une opportunité en format Excel."""
    try:
        # Créer le dossier exports s'il n'existe pas
        export_dir = PathLib("exports")
        export_dir.mkdir(exist_ok=True)
        
        output_path = export_dir / f"opportunity_{opportunity_id}.xlsx"
        
        if service.to_excel(opportunity_id, str(output_path)):
            return FileResponse(
                path=str(output_path),
                filename=f"opportunity_{opportunity_id}.xlsx",
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            raise HTTPException(status_code=404, detail="Impossible d'exporter l'opportunité")
            
    except Exception as e:
        logger.error(f"Erreur lors de l'export de l'opportunité: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))