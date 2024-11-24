```markdown
# Gestionnaire d'Opportunités

Une application web permettant de gérer et d'analyser les opportunités commerciales pour les prêts immobiliers.

## Fonctionnalités

- Recherche d'opportunités par ID
- Recherche avancée avec filtres (âge, revenu, banque)
- Affichage détaillé des informations d'une opportunité
- Visualisation des propositions commerciales associées
- Export des données au format Excel

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Navigateur web moderne

## Installation

1. Cloner le repository :
```bash
git clone [URL_DU_REPO]
cd opportunity_manager
```

2. Créer un environnement virtuel :
```bash
python -m venv env
source env/bin/activate  # Sur Unix/macOS
# ou
env\Scripts\activate     # Sur Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Structure des données

L'application attend deux fichiers CSV dans le dossier `data_sources/gold/` :
- `opportunities_cleaned.csv` : Données des opportunités
- `propositions_cleaned.csv` : Données des propositions commerciales

## Démarrage

1. Lancer le serveur :
```bash
uvicorn app.main:app --reload
```

2. Accéder à l'application :
Ouvrir un navigateur et aller à `http://localhost:8000`

## Structure du projet

```
opportunity_manager/
│
├── app/
│   ├── models/
│   │   └── opportunity.py
│   ├── routes/
│   │   ├── opportunities.py
│   │   └── health.py
│   ├── services/
│   │   ├── opportunity_service.py
│   │   └── opportunity_validator.py
│   ├── templates/
│   │   └── index.html
│   └── main.py
│
├── data_sources/
│   └── gold/
│       ├── opportunities_cleaned.csv
│       └── propositions_cleaned.csv
│
├── static/
│   ├── style.css
│   └── script.js
│
├── tests/
│   └── test_opportunity_service.py
│
├── exports/           # Dossier pour les exports Excel
├── requirements.txt
└── README.md
```

## API Documentation

L'API documentation est disponible à `http://localhost:8000/docs`

Endpoints principaux :
- `GET /opportunities/{id}` : Obtenir une opportunité par ID
- `GET /opportunities/search` : Recherche avancée
- `GET /opportunities/{id}/export` : Exporter une opportunité en Excel

## Tests

Pour exécuter les tests :
```bash
pytest tests/
```

## Développement

Pour vérifier la qualité des données :
```bash
python check_data.py
```

Pour vérifier la configuration :
```bash
python check_setup.py
```

## Technologies utilisées

- FastAPI : Framework web rapide pour construire des APIs
- Pandas : Manipulation et analyse de données
- Pydantic : Validation des données
- Uvicorn : Serveur ASGI pour Python
- OpenPyXL : Gestion des fichiers Excel

## Auteurs

- Serges ADJOMO

```

