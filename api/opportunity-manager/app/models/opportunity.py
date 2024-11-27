# Chemin: app/models/opportunity.py

from pydantic import BaseModel, Field
from typing import Optional, List

class InformationsPrincipales(BaseModel):
    age: Optional[float] = None
    revenu_mensuel: Optional[float] = None
    banque: Optional[str] = None

class MontantProjet(BaseModel):
    pret_principal: Optional[float] = None
    apport_personnel: Optional[float] = None
    travaux: Optional[float] = None

class Situation(BaseModel):
    actuelle: Optional[str] = None
    taux_endettement: Optional[float] = None
    charges_mensuelles: Optional[float] = None

class DetailsComplementaires(BaseModel):
    type_bien: Optional[str] = None
    usage_bien: Optional[str] = None
    type_projet: Optional[str] = None
    montant_projet: Optional[MontantProjet] = None
    situation: Optional[Situation] = None

class Proposition(BaseModel):
    taux: Optional[float] = None
    duree_mois: Optional[float] = None
    etape: Optional[str] = None

class OpportunityResponse(BaseModel):
    informations_principales: Optional[InformationsPrincipales] = None
    est_exploitable: bool
    raisons_non_exploitable: Optional[List[str]] = None
    details_complementaires: Optional[DetailsComplementaires] = None
    propositions: Optional[List[Proposition]] = None