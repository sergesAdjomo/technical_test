
# Documentation Technique - Dossier Services

## Structure du Dossier
```
app/services/
├── opportunity_service.py
└── opportunity_validator.py
```

## opportunity_service.py
Service principal pour la gestion des opportunités commerciales.

### Composants Principaux
- **OpportunityInfoService**: Classe principale du service
- **Dépendances**:
  - pandas: Pour la manipulation des données
  - OpportunityValidator: Pour la validation des opportunités

### Initialisation
```python
def __init__(self, data_path: str)
```
- Charge les données depuis deux fichiers CSV:
  - opportunities_cleaned.csv
  - propositions_cleaned.csv
- Convertit les colonnes numériques appropriées
- Configure le logging

### Méthodes Principales

#### 1. get_info
```python
def get_info(self, opportunity_id: str, include_propositions: bool = False) -> Dict
```
- Récupère les informations détaillées d'une opportunité
- Paramètres:
  - opportunity_id: Identifiant de l'opportunité
  - include_propositions: Option pour inclure les propositions
- Retourne un dictionnaire avec les informations formatées

#### 2. search_opportunities
```python
def search_opportunities(
    self,
    age_min: Optional[int] = None,
    age_max: Optional[int] = None,
    revenu_min: Optional[float] = None,
    banque: Optional[str] = None,
    limit: int = 10
) -> List[Dict]
```
- Recherche des opportunités selon des critères
- Applique les filtres successivement
- Retourne une liste d'opportunités formatées

#### 3. to_excel
```python
def to_excel(self, opportunity_id: str, output_path: str) -> bool
```
- Exporte les informations d'une opportunité vers Excel
- Crée un fichier Excel formaté
- Retourne True si succès, False sinon

## opportunity_validator.py
Module de validation des opportunités.

### Composants Principaux
- **OpportunityValidator**: Classe de validation
- **Méthode Principale**: validate_opportunity

### Règles de Validation
1. **Données obligatoires**:
   - Age de l'emprunteur
   - Revenu total
   - Banque principale

2. **Validations numériques**:
   - Montants non négatifs
   - Âge entre 18 et 85 ans
   - Revenu minimum 1000€
   - Taux d'endettement max 35%

3. **Validations de statut**:
   - Vérifie si l'opportunité n'est pas déjà perdue

### Points d'Attention
1. **Gestion des données**:
   - Utilisation de pandas pour la manipulation efficace
   - Conversion des types de données appropriée
   - Gestion des valeurs manquantes

2. **Performance**:
   - Les données sont chargées une seule fois à l'initialisation
   - Utilisation de filtres pandas optimisés
   - Limitation du nombre de résultats

3. **Maintenance**:
   - Logging détaillé pour le débogage
   - Structure modulaire pour faciliter les modifications
   - Validation séparée de la logique métier

4. **Sécurité**:
   - Validation des entrées
   - Gestion des erreurs robuste
   - Protection contre les injections de données invalides

---

## Conclusion :
Le service `OpportunityInfoService` fournit des fonctionnalités essentjsonantes pour la gestion des opportunités commerciales. Il est conçu pour être robuste, performant et sécurisé. La validation des opportunités est gérée par le module `OpportunityValidator`, qui garantit l'intégrité des données et la conformité aux règles métier. Ces composants sont essentiels pour le bon fonctionnement de l'application Opportunity Manager.
```
   
