# Documentation Technique - Tests

## Structure du Dossier
```
tests/
└── test_opportunity_service.py
```

## test_opportunity_service.py
Ce fichier implémente les tests unitaires pour le service OpportunityInfoService.

### Technologies Utilisées
- **pytest**: Framework de test
- **pandas**: Manipulation des données de test
- **fixtures**: Création d'environnements de test isolés

### Configuration des Tests

#### Fixture Principal
```python
@pytest.fixture
def service(self, tmp_path):
```
Cette fixture configure l'environnement de test avec :
- Création d'un répertoire temporaire (`tmp_path`)
- Génération de données de test pour :
  - Opportunités
    ```python
    opportunities_data = {
        'id': ['123', '456'],
        'age': [30, 45],
        'revenu_total': [50000, 75000],
        'banque_principale': ['BNP', 'SG']
    }
    ```
  - Propositions
    ```python
    propositions_data = {
        'opportunity_id': ['123', '123'],
        'montant': [100000, 150000],
        'taux': [2.5, 2.7],
        'duree': [240, 300],
        'mensualite': [500, 600]
    }
    ```

### Cas de Tests

#### 1. Récupération d'Opportunité Valide
```python
def test_get_info_valid_opportunity(self, service)
```
**Objectif**: Vérifier la récupération correcte d'une opportunité existante
- **Vérifications**:
  - État d'exploitation
  - Âge du client
  - Revenu total
  - Banque principale
  - Absence de propositions non demandées

#### 2. Récupération avec Propositions
```python
def test_get_info_with_propositions(self, service)
```
**Objectif**: Vérifier l'inclusion des propositions associées
- **Vérifications**:
  - Présence des propositions
  - Nombre correct de propositions
  - Données des propositions

#### 3. Gestion des Opportunités Invalides
```python
def test_get_info_invalid_opportunity(self, service)
```
**Objectif**: Vérifier le comportement avec un ID inexistant
- **Vérifications**:
  - État d'exploitation à False
  - Message d'erreur approprié

#### 4. Cas Limites
```python
def test_edge_cases()
```
**Objectif**: Vérifier le comportement aux limites acceptables
- **Cas testés**:
  - Âge minimum (18 ans)
  - Âge maximum (85 ans)
  - Validation des données obligatoires

#### 5. Export Excel
```python
def test_to_excel(self, service, tmp_path)
```
**Objectif**: Vérifier la fonctionnalité d'export Excel
- **Vérifications**:
  - Création du fichier
  - Présence des onglets requis
  - Structure des données exportées

### Bonnes Pratiques Implémentées

1. **Isolation des Tests**
   - Utilisation de `tmp_path` pour les fichiers temporaires
   - Données de test indépendantes pour chaque test
   - Nettoyage automatique après les tests

2. **Organisation du Code**
   - Tests groupés par fonctionnalité
   - Noms de tests descriptifs
   - Documentation claire des objectifs

3. **Données de Test**
   - Jeu de données minimal mais représentatif
   - Cas normaux et limites couverts
   - Données structurées de manière cohérente

4. **Assertions**
   - Vérifications précises et ciblées
   - Messages d'erreur explicites
   - Couverture des cas positifs et négatifs

### Points d'Attention

1. **Maintenance**
   - Les données de test doivent rester synchronisées avec le modèle de données
   - Les cas limites doivent être mis à jour si les règles métier changent
   - Les chemins de fichiers doivent être gérés de manière portable

2. **Performance**
   - Les fixtures sont réutilisées efficacement
   - Les fichiers temporaires sont nettoyés
   - Les tests sont indépendants et peuvent s'exécuter en parallèle

3. **Couverture**
   - Tests des fonctionnalités principales
   - Vérification des cas d'erreur
   - Validation des contraintes métier

4. **Extensibilité**
   - Structure permettant d'ajouter facilement de nouveaux cas de test
   - Possibilité d'étendre les données de test
   - Support pour de nouvelles fonctionnalités

### Commandes Utiles

Pour exécuter les tests :
```bash
# Exécuter tous les tests
pytest

# Exécuter avec détails
pytest -v

# Exécuter avec couverture de code
pytest --cov=app tests/

# Exécuter un test spécifique
pytest tests/test_opportunity_service.py::TestOpportunityInfoService::test_get_info_valid_opportunity
```
