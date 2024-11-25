
---

# **Gestionnaire d'Opportunités**

Bienvenue dans le **Gestionnaire d'Opportunités**, une application web permettant de gérer et d’analyser les opportunités commerciales dans le domaine des prêts immobiliers. Elle offre une interface utilisateur moderne, une API robuste et des outils d’exportation pour faciliter la gestion des données.

---

## **Fonctionnalités Principales**

- **Recherche d’opportunités par identifiant** avec option d'inclure les propositions commerciales associées.
- **Recherche avancée** avec filtres : âge, revenu, banque, etc.
- **Évaluation de l'exploitabilité** d’une opportunité.
- **Export des données** en format Excel.
- **Vérification de la qualité des données** via des scripts utilitaires.
- **Endpoint de vérification de la santé** de l’application.
- **Documentation Swagger** intégrée pour explorer les endpoints API.

---

## **Prérequis**

1. **Méthode traditionnelle :**
   - Python 3.8 ou version ultérieure (Python 11 recommandé pour certaines fonctionnalités).
   - Pip pour gérer les dépendances Python.

2. **Méthode Docker (recommandée) :**
   - Docker installé sur votre machine.

---

## **Installation et Configuration**

### Méthode 1 : Installation Traditionnelle
1. **Cloner le projet :**
   ```bash
   git clone https://github.com/sergesAdjomo/technical_test/
   cd opportunity_manager
   ```

2. **Créer un environnement virtuel :**
   ```bash
   python -m venv env
   source env/bin/activate  # Unix/macOS
   env\Scripts\activate     # Windows
   ```

3. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l’application :**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Accéder à l’application :** Ouvrez `http://127.0.0.1:8000` dans votre navigateur.

---

### Méthode 2 : Utilisation avec Docker (Recommandée)
1. **Construire et lancer l’application :**
   ```bash
   docker-compose up --build
   ```

2. **Accéder à l’application :** Ouvrez `http://127.0.0.1:8000` dans votre navigateur.

3. **Arrêter l’application :**
   ```bash
   docker-compose down
   ```
---

### Méthode 3 : Utilisation avec le Script de Démarrage (start.bat / start.sh)
1. **Exécuter le script de démarrage :**
   - **Windows :** Double-cliquez sur `start.bat`.
   - **Unix/macOS :** Exécutez `./start.sh` (Assurez-vous de donner les permissions nécessaires) avec `bash start.sh`.
   - **Accéder à l’application :** Ouvrez `http://127.0.0.1:8000` dans votre navigateur.

---

## **Structure du Projet**

```
opportunity_manager/
├── app/
│   ├── models/                  # Modèles de données
│   ├── routes/                  # Endpoints API
│   ├── services/                # Logique métier
│   ├── templates/               # Fichiers HTML
│   └── main.py                  # Point d’entrée
├── data_sources/                # Données sources
│   └── gold/                    # Fichiers CSV sources
├── tests/                       # Tests unitaires et fonctionnels
├── utils/                       # Scripts utilitaires
├── static/                      # CSS et JavaScript
├── exports/                     # Fichiers Excel générés
├── Dockerfile                   # Définition du conteneur Docker
├── docker-compose.yml           # Orchestration multi-conteneurs
├── start.bat / start.sh         # Scripts de démarrage
└── requirements.txt             # Dépendances Python
```

---

## **Utilisation**

### Recherche d'une opportunité :
1. Entrez l’identifiant de l’opportunité dans l’interface.
2. Activez l’option **Inclure les propositions** pour voir les propositions associées.
3. Cliquez sur **Rechercher**.

### Export des données :
- Cliquez sur **Exporter en Excel** pour télécharger les informations.
- Les fichiers exportés se trouvent dans :
  - Le dossier `exports/`.
  - Ou directement dans le dossier de téléchargement de votre machine.

---

## **Documentation API**

Accessible via Swagger à l'adresse :
```
http://127.0.0.1:8000/docs
```

### Endpoints Clés
1. **Recherche par ID :**
   - `GET /opportunities/{id}`
   - Paramètre : `include_propositions` (optionnel).

2. **Recherche avancée :**
   - `GET /opportunities/search`
   - Filtres : `age_min`, `age_max`, `revenu_min`, `banque`, etc.

3. **Export Excel :**
   - `GET /opportunities/{id}/export`.

4. **Vérification de l'état de l'API :**
   - `GET /health/`.

---

## **Tests**

Les tests sont situés dans le dossier `tests/`.

### Exécuter les tests :
```bash
pytest
```

### Couverture des tests :
```bash
pytest --cov=app
```

---

## **Scripts Utilitaires**

1. **Validation des données :**
   - `utils/check_data.py` : Vérifie la présence des données requises.
   - `utils/data_quality.py` : Évalue la qualité des données CSV.

2. **Vérification de la structure :**
   - `utils/check_setup.py` : Valide la configuration du projet.

---

## **Support**

Pour toute question, contactez :
📧 **sergesadjomo54@gmail.com**

--- 

Si vous avez des suggestions d'amélioration, faites-les-nous savoir. 🚀