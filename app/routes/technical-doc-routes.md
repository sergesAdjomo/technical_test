# Documentation Technique - Dossier Routes

## Structure du Dossier
```
app/routes/
├── health.py
└── opportunities.py
```

## health.py
Ce fichier implémente les routes de santé (healthcheck) de l'API.

### Composants Principaux
- **Router**: Utilise `APIRouter()` de FastAPI
- **Endpoint**: `/health/`
  - **Méthode**: GET
  - **Description**: Vérifie l'état de fonctionnement de l'API
  - **Retour**: JSON avec status et version de l'API

### Exemple de Réponse
```json
{
    "status": "healthy",
    "version": "1.0.0"
}
```

## opportunities.py
Implémente les routes de gestion des opportunités commerciales.

### Composants Principaux
- **Router**: Instance de `APIRouter()`
- **Service**: Utilise `OpportunityInfoService` avec le chemin "data_sources/gold"
- **Logger**: Configuration du logging pour le suivi des opérations

### Routes Implémentées

#### 1. Recherche Avancée
- **Endpoint**: `/opportunities/search`
- **Méthode**: GET
- **Paramètres**:
  - `age_min` (optionnel): Âge minimum
  - `age_max` (optionnel): Âge maximum
  - `revenu_min` (optionnel): Revenu minimum mensuel
  - `banque` (optionnel): Banque principale
  - `limit` (default=10): Nombre maximum de résultats
- **Retour**: Liste d'`OpportunityResponse`

#### 2. Récupération par ID
- **Endpoint**: `/opportunities/{opportunity_id}`
- **Méthode**: GET
- **Paramètres**:
  - `opportunity_id` (obligatoire): ID de l'opportunité
  - `include_propositions` (optionnel, default=False): Inclure les propositions
- **Retour**: `OpportunityResponse`

#### 3. Export Excel
- **Endpoint**: `/opportunities/{opportunity_id}/export`
- **Méthode**: GET
- **Paramètres**:
  - `opportunity_id` (obligatoire): ID de l'opportunité
- **Retour**: Fichier Excel
- **Particularités**:
  - Crée un dossier 'exports' si non existant
  - Génère un fichier Excel nommé `opportunity_{id}.xlsx`
  - Utilise `FileResponse` pour le téléchargement

### Gestion des Erreurs
- Utilisation de try/catch sur toutes les routes
- Logging détaillé des erreurs
- Retours d'erreurs HTTP appropriés:
  - 404: Ressource non trouvée
  - 500: Erreur serveur interne

### Points d'Attention
1. L'ordre des routes est important:
   - La route `/search` doit être définie avant la route `/{opportunity_id}`
   - Évite les conflits de routage FastAPI

2. Logging:
   - Chaque opération importante est loggée
   - Les erreurs sont loggées avec le niveau ERROR
   - Les warnings sont utilisés pour les cas non-critiques

3. Sécurité:
   - Les paramètres sont validés via FastAPI
   - Les valeurs limites sont définies pour certains paramètres (ex: limit entre 1 et 100)

4. Performance:
   - Les opérations asynchrones sont utilisées (async/await)
   - Le streaming de fichiers est géré par FileResponse

---

## Conclusion : 
Le dossier `routes` contient les définitions des routes de l'API, avec des fonctionnalités de recherche, de récupération et d'export de données d'opportunités commerciales. Les routes sont conçues pour être robustes, sécurisées et performantes, en utilisant les fonctionnalités avancées de FastAPI et des services associés. Le logging est utilisé de manière extensive pour assurer le suivi des opérations et des erreurs. Les routes sont conçues pour être extensibles et maintenables, en suivant les meilleures pratiques de développement d'API RESTful.
[]: # (end)
