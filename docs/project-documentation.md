# Gestionnaire d'Opportunités - Documentation Technique Complète

## Vue d'Ensemble de l'Architecture

L'application suit une architecture de traitement de données moderne avec les composants suivants dans l'ordre du flux de données :

1. **Stockage des Données Source (GCS)**
   - Bucket pour les fichiers de données brutes
   - Bucket pour les schémas JSON
   - Bucket pour le code source Cloud Function

2. **Pipeline de Chargement (Cloud Function)**
   - Déclenchement automatique sur l'ajout de fichiers
   - Validation des schémas
   - Chargement dans BigQuery

3. **Transformation des Données (dbt)**
   - Nettoyage et structuration
   - Création de tables dérivées
   - Contrôles de qualité

4. **API (Cloud Run)**
   - Interface RESTful
   - Accès aux données nettoyées
   - Export et analyses

## Infrastructure Cloud (GCP)

### Configuration GCS
- Bucket `data-files-01`: Fichiers source
- Bucket `e-datacap-schemas`: Définitions des schémas
- Bucket `gcf-source-001`: Code source Cloud Function

### BigQuery
Dataset: `ds_etl`
Tables:
- Raw data: Correspond aux noms des fichiers source
- Tables nettoyées: Suffixe `_cleaned`

### Transformations dbt

```sql
-- opportunities_cleaned.sql
WITH source AS (
    SELECT *
    FROM ${ref('opportunities')}
),

validated_opportunities AS (
    SELECT *
    FROM source
    WHERE 
        -- Validation des champs critiques
        TotRev__c > 0 
        AND Age_emprunteur__c BETWEEN 18 AND 80
        AND BanquePrincipaleEmp__c IS NOT NULL
),

cleaned AS (
    SELECT
        Id,
        CreatedDate,
        Age_emprunteur__c AS age,
        TotRev__c AS revenu_total,
        TotCharges__c AS charges_totales,
        BanquePrincipaleEmp__c AS banque_principale,
        MontPretPricip__c AS montant_pret,
        -- Calcul du taux d'endettement
        SAFE_DIVIDE(TotCharges__c, TotRev__c) * 100 AS taux_endettement,
        -- Marquage des opportunités exploitables
        CASE 
            WHEN TotRev__c >= 1000 
                AND SAFE_DIVIDE(TotCharges__c, TotRev__c) <= 0.35 
            THEN TRUE 
            ELSE FALSE 
        END AS exploitable
    FROM validated_opportunities
)

SELECT * FROM cleaned
```

```sql
-- propositions_cleaned.sql
WITH source AS (
    SELECT *
    FROM ${ref('propositions')}
),

validated_propositions AS (
    SELECT *
    FROM source
    WHERE 
        -- Validation des taux et durée
        TXHA__c > 0 
        AND TauxAss__c > 0
        AND DureePret_Mois__c > 0
        -- Exclusion des propositions non éligibles
        AND NOT CONTAINS_SUBSTR(Etape_Source__c, 'Non éligible')
),

cleaned AS (
    SELECT
        Id,
        Opportunity__c,
        Partenaire__c,
        TXHA__c AS taux_hors_assurance,
        TauxAss__c AS taux_assurance,
        DureePret_Mois__c AS duree_pret,
        CreatedDate,
        -- Calcul du coût total
        (TXHA__c + TauxAss__c) * DureePret_Mois__c / 1200 AS cout_total
    FROM validated_propositions
)

SELECT * FROM cleaned
```

## API FastAPI

### Fonctionnalités Principales

1. **Recherche d'Opportunités**
```python
@router.get("/opportunities/search")
async def search_opportunities(
    age_min: Optional[int] = None,
    age_max: Optional[int] = None,
    revenu_min: Optional[float] = None,
    banque: Optional[str] = None,
    limit: int = Query(default=10, le=100)
):
```

2. **Détail d'une Opportunité**
```python
@router.get("/opportunities/{opportunity_id}")
async def get_opportunity(
    opportunity_id: str,
    include_propositions: bool = False
):
```

3. **Export Excel**
```python
@router.get("/opportunities/{opportunity_id}/export")
async def export_opportunity(opportunity_id: str):
```

### Structure du Projet
```
opportunity_manager/
├── app/
│   ├── models/          # Modèles de données
│   ├── routes/          # Points d'accès API
│   ├── services/        # Logique métier
│   └── main.py         # Point d'entrée
├── infrastructure/      # Code Terraform
├── dbt/                # Transformations dbt
└── cloud_function/     # Code Cloud Function
```

## Installation et Déploiement

### 1. Infrastructure (Terraform)
```bash
cd infrastructure
terraform init
terraform plan
terraform apply
```

### 2. Déploiement dbt
```bash
cd dbt
dbt deps
dbt run --profiles-dir .
```

### 3. API (Docker)
```bash
docker build -t mt-test-repo/api .
docker push mt-test-repo/api
gcloud run deploy
```

## Utilisation de l'API

### Endpoint Documentation
- Documentation Swagger: `http://HOST:PORT/docs`
- Healthcheck: `http://HOST:PORT/health`

### Exemples de Requêtes

1. Recherche d'opportunités:
```bash
curl "http://HOST:PORT/opportunities/search?age_min=25&age_max=45&revenu_min=3000"
```

2. Détail avec propositions:
```bash
curl "http://HOST:PORT/opportunities/OPP123?include_propositions=true"
```

## Maintenance et Monitoring

### Logs et Surveillance
- Cloud Function: Cloud Logging
- BigQuery: Audit logs et métriques d'utilisation
- API: Cloud Run metrics

### Sécurité
- IAM: Rôles et permissions strictement définis
- Encryption: Données chiffrées au repos et en transit
- Validation: Contrôles d'entrée sur tous les endpoints

## Support et Contact

Pour toute question technique:
- Email: sergesadjomo54@gmail.com
- Documentation API: `/docs`
- Logs: Cloud Logging Console

---

Cette documentation couvre l'ensemble du pipeline de données, depuis l'ingestion jusqu'à l'exposition via l'API. Le système est conçu pour être modulaire, scalable et maintainable, avec une attention particulière portée à la qualité des données et à la sécurité.
