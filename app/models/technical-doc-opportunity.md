# Documentation du Dossier Models

## opportunity.py

Ce fichier définit les modèles de données Pydantic pour la gestion des opportunités de prêt immobilier.

### Classes

#### InformationsPrincipales
Représente les informations essentielles d'un emprunteur.
- `age` (float, optionnel) : Âge de l'emprunteur
- `revenu_mensuel` (float, optionnel) : Revenu mensuel de l'emprunteur
- `banque` (str, optionnel) : Banque principale de l'emprunteur

#### MontantProjet
Détaille les aspects financiers du projet immobilier.
- `pret_principal` (float, optionnel) : Montant du prêt principal demandé
- `apport_personnel` (float, optionnel) : Montant de l'apport personnel
- `travaux` (float, optionnel) : Montant prévu pour les travaux

#### Situation
Décrit la situation financière actuelle de l'emprunteur.
- `actuelle` (str, optionnel) : Situation actuelle (ex: locataire, propriétaire)
- `taux_endettement` (float, optionnel) : Taux d'endettement actuel
- `charges_mensuelles` (float, optionnel) : Montant des charges mensuelles

#### DetailsComplementaires
Regroupe les informations complémentaires sur le projet.
- `type_bien` (str, optionnel) : Type de bien (ex: appartement, maison)
- `usage_bien` (str, optionnel) : Usage prévu du bien
- `type_projet` (str, optionnel) : Type de projet immobilier
- `montant_projet` (MontantProjet, optionnel) : Détails financiers du projet
- `situation` (Situation, optionnel) : Situation financière détaillée

#### Proposition
Représente une proposition de financement.
- `taux` (float, optionnel) : Taux d'intérêt proposé
- `duree_mois` (float, optionnel) : Durée du prêt en mois
- `etape` (str, optionnel) : État actuel de la proposition

#### OpportunityResponse
Modèle principal de réponse pour une opportunité.
- `informations_principales` (InformationsPrincipales, optionnel) : Informations de base
- `est_exploitable` (bool) : Indique si l'opportunité est exploitable
- `raisons_non_exploitable` (List[str], optionnel) : Liste des raisons si non exploitable
- `details_complementaires` (DetailsComplementaires, optionnel) : Détails du projet
- `propositions` (List[Proposition], optionnel) : Liste des propositions de financement

### Utilisation
Ces modèles sont utilisés pour :
- Valider les données entrantes
- Structurer les réponses de l'API
- Assurer la cohérence des données dans l'application

### CONCLUSION
Ce fichier contient les modèles de données Pydantic pour la gestion des opportunités de prêt immobilier. Ces classes permettent de structurer les informations entrantes et sortantes. Elles garantissent la cohérence des données et facilitent le développement de l'application.

[]: # (END)
```