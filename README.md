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

4. **API (Cloud Run)** LIEN POUR ACCEDER A L'API / https://manager-op-717746004167.us-central1.run.app
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
├───api                   # Contient le code de l'application API
│   ├───app              # Dossier principal de l'application
│   │   ├───models       # Définition des modèles de données
│   │   ├───routes       # Gestion des routes et des endpoints
│   │   ├───services     # Logique métier et services externes
│   │   └───templates    # Fichiers HTML/css/js
│   ├───tests            # Tests unitaires pour l'API
│   └───utils            # Fonctions utilitaires réutilisables
├───dbt                   # Configuration et transformations SQL
│   ├───models           # Modèles dbt pour les données transformées
│   │   ├───cleaned      # requette de nettoyage
│   │   └───example      # Modèles d'exemple
│   └───tests            # Tests de qualité des données
├───infra                 # Scripts d'infrastructure
│   ├───bigquery-dataset # Configuration des datasets BigQuery
│   ├───cloud-function   # Déploiement des Google Cloud Functions
│   └───cloud-storage    # Configuration des buckets GCS
├───logs                  # Logs d'exécution des pipelines
├───data_sources          # Sources de données brutes ou externes
└───docs                  # Documentation et spécifications
|___.github/workflows     # Workflows CI/CD




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



## Architecture Améliorée

Cette section décrit l'architecture complète du pipeline de traitement des données, comme illustré dans l'image fournie.

### Description des Composants

1. **Google Cloud Storage (GCS)**  
   Les données brutes sont chargées dans des buckets GCS. Chaque fichier déposé déclenche un pipeline pour traitement ultérieur.

2. **BigQuery Load (bq-load)**  
   Une étape automatique charge les données depuis GCS dans une table `raw-data` de BigQuery.

3. **DBT (Data Build Tool)**  
   DBT est utilisé pour transformer les données stockées dans la table `raw-data` en données nettoyées et modélisées dans une table `cleaned-data`. Cela permet de maintenir une couche analytique fiable pour des requêtes complexes.

4. **API**  
   Une API est connectée pour interagir avec la couche des données transformées, permettant ainsi des intégrations ou analyses en temps réel.

### Flux des Données

- Les fichiers sont initialement stockés dans GCS.
- Ils sont ensuite lus et chargés dans BigQuery (`raw-data`) via un pipeline `bq-load`.
- DBT exécute des transformations SQL sur les données pour produire des tables prêtes à l'analyse (`cleaned-data`).
- Une API finale exploite ces données transformées pour fournir des fonctionnalités ou insights à l'utilisateur final.

### Illustration

L'architecture suivante montre visuellement ce flux :
![Architecture du Pipeline](image.png)

---

Cette configuration garantit un traitement de données fluide et reproductible, en combinant le meilleur des outils GCP et DBT pour des performances optimales.
