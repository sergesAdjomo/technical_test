# Documentation des Scripts Utilitaires

## 1. `check_data.py`

Ce script contient la fonction `check_data()` qui assure la vérification et la création des fichiers de données nécessaires.

**Chemin** : Racine du projet

### Fonction `check_data()`
- **Vérification des fichiers** : Vérifie l'existence des fichiers `opportunities_cleaned.csv` et `propositions_cleaned.csv` dans le dossier `data_sources/gold`.
- **Lecture des données** : Si les fichiers existent, les lit avec `pandas` et les affiche.
- **Création des fichiers** : Si les fichiers n'existent pas, crée le dossier `data_sources/gold` si nécessaire, génère des données de test et les sauvegarde dans les fichiers CSV correspondants.

## 2. `check_setup.py`

Ce script contient la fonction `check_structure()` qui vérifie la conformité de la structure du projet par rapport à une structure attendue.

**Chemin** : Racine du projet

### Fonction `check_structure()`
- **Définition de la structure** : Définit la structure attendue du projet sous forme de dictionnaire imbriqué.
- **Vérification récursive** : Parcourt la structure attendue et vérifie l'existence de chaque dossier et fichier.
- **Gestion des erreurs** : Affiche un message d'erreur pour chaque dossier ou fichier manquant.
- **Création automatique** : Crée automatiquement le dossier `data_sources/gold` s'il est manquant.
- **Messages de succès** : Affiche un message de succès pour chaque dossier et fichier trouvé.

## 3. `data_quality.py`

Ce script contient la fonction `check_data_quality()` qui évalue la qualité des données d'un DataFrame pandas.

**Chemin** : Non spécifié (nouveau fichier)

### Fonction `check_data_quality(df: pd.DataFrame) -> Dict[str, List[str]]`
- **Entrée** : Prend en entrée un DataFrame pandas `df`.
- **Initialisation** : Initialise un dictionnaire `issues` pour stocker les problèmes de qualité des données.
- **Analyse des colonnes** : Parcourt chaque colonne du DataFrame et compte les valeurs manquantes.
- **Rapport des problèmes** : Ajoute un message d'erreur à `issues['missing_values']` pour chaque colonne avec des valeurs manquantes.
- **Retour** : Retourne le dictionnaire `issues` contenant les problèmes de qualité des données.

---

En résumé, les scripts `check_data.py`, `check_setup.py` et `data_quality.py` fournissent des fonctions essentielles pour vérifier la structure du projet, l'existence des fichiers de données et la qualité des données. Ils garantissent que le projet est correctement configuré et que les données sont prêtes à être utilisées dans l'application principale.
