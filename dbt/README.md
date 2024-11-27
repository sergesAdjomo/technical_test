---
---

# Projet ETL avec dbt et BigQuery

## Description

Ce projet utilise **dbt** pour orchestrer les transformations de données dans **BigQuery**. 
dbt est intégré dans un pipeline **CI/CD GitLab**, où il est exécuté manuellement après la réalisation des étapes préalables. 
Le traitement utilise les configurations de connexion Google Cloud Platform (GCP) via les variables d'environnement et gcloud.

## Arborescence du projet dbt

Le répertoire dbt du projet est structuré comme suit :

```
├── dbt_project.yml          # Fichier de configuration principal du projet dbt
├── models/                  # Contient les modèles dbt
│   ├── example/             # Exemple de modèles SQL
│   ├── elimination_doublons.sql
│   ├── filtrage_mentions.sql
│   ├── fusion_pubmed.sql
│   ├── journal_max_mentions.sql
│   ├── mags_pubmed_pas_clinical.sql
│   ├── ...
├── macros/                  # Macros personnalisées en Jinja
├── snapshots/               # Gestion des snapshots (historisation des données)
├── tests/                   # Tests personnalisés
├── seeds/                   # Données statiques si besoin
├── profiles.yml             # Fichier de configuration des connexions à BigQuery
├── requirements.txt         # Fichier listant les dépendances (dbt-core, dbt-bigquery)
└── ...
```

### Configuration gcloud pour l'authentification à GCP

L'authentification à GCP via **gcloud** est réalisée avant l'exécution des modèles dbt à l'aide des commandes suivantes dans la pipeline GitLab :

```bash
# Configurer le projet GCP
gcloud config set project $GCP_PROJECT_ID

# Configurer le compte de service
gcloud config set account $GCP_SERVICE_ACCOUNT

# Activer le compte de service avec les credentials
gcloud auth activate-service-account --key-file $GOOGLE_CREDENTIALS
```

### Fichier `profiles.yml`

Le fichier `profiles.yml` contient la configuration spécifique à dbt pour la connexion à BigQuery :

```yaml
default:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: "{{ env_var('GCP_PROJECT_ID') }}"
      dataset: ds_etl
      threads: 4
      location: us-central1
      priority: interactive
      timeout_seconds: 300
```

### Fichier `.gitlab-ci.yml`

Le fichier `.gitlab-ci.yml` contient la configuration spécifique à dbt pour l'exécution des modèles dans la pipeline GitLab :

```yaml
dbt-run:
  stage: dbt-pipelines
  when: manual
  image: python:3.12  # Utilisation de Python 3.12 pour gérer dbt et les dépendances
  needs:
    - copy-files  # Nécessite que les fichiers aient été copiés dans GCS
  script:
    - echo "Vérification de la version de Python et de Pip"
    - python --version  # Vérification de la version de Python
    - pip install --upgrade pip  # Mise à jour de pip
    - echo "Installation de jq pour le traitement JSON"
    - apt-get update && apt-get install -y jq  # Installation de jq
    - echo "Affichage du chemin ou contenu de la variable GOOGLE_CREDENTIALS"
    - if [ -f "$GOOGLE_CREDENTIALS" ]; then cat "$GOOGLE_CREDENTIALS"; else echo "$GOOGLE_CREDENTIALS"; fi
    - echo "Enregistrement du fichier de clé JSON"
    - if [ -f "$GOOGLE_CREDENTIALS" ]; then cp "$GOOGLE_CREDENTIALS" /tmp/keyfile.json; else echo "$GOOGLE_CREDENTIALS" | jq '.' > /tmp/keyfile.json; fi
    - echo "Affichage du contenu du fichier JSON"
    - cat /tmp/keyfile.json  # Imprimer le contenu pour vérifier
    - echo "Se déplacer dans le répertoire dbt"
    - cd dbt  # Se déplacer dans le répertoire dbt
    - echo "Création et activation de l'environnement virtuel"
    - python -m venv venv  # Création de l'environnement virtuel
    - source venv/bin/activate  # Activation de l'environnement virtuel
    - echo "Installation des dépendances à partir de requirements.txt"
    - pip install -r requirements.txt  # Installation des dépendances dbt
    - echo "Initialisation de DBT et vérification de la configuration"
    - dbt debug --profiles-dir .  # Vérification des configurations DBT
    - echo "Exécution de dbt build"
    - dbt build --profiles-dir .  # Exécution des transformations dbt
```


Ici, nous utilisons des variables d’environnement pour la configuration du projet et l’authentification.

## Installation des dépendances

Le fichier `requirements.txt` contient les dépendances nécessaires à dbt et à ses connecteurs :

```bash
python==3.12
dbt-core==1.0.0
dbt-bigquery==1.0.0
```

Pour installer ces dépendances dans la pipeline ou localement, exécutez :

```bash
pip install -r requirements.txt
```

## Exécution des modèles dbt

Une fois les dépendances installées et l'authentification effectuée, dbt peut être exécuté manuellement dans la pipeline GitLab après que les étapes précédentes ont été réalisées (comme le chargement de fichiers dans GCS).

---

### **Utilisation de jq et Sécurité**

Dans cette pipeline, nous utilisons l'outil **jq** pour gérer les fichiers JSON et manipuler les credentials Google Cloud de manière sécurisée.

#### **Pourquoi utiliser jq ?**

`jq` est un outil léger pour traiter et manipuler des données JSON. Il est utilisé ici pour les raisons suivantes :

1. **Validation du JSON** : Nous vérifions que le contenu de la variable d'environnement `$GOOGLE_CREDENTIALS` est bien formaté en JSON avant de l'utiliser. Cela permet d'éviter des erreurs de format qui pourraient entraîner des échecs dans la pipeline.

2. **Transformation JSON** : Si nécessaire, `jq` peut aussi être utilisé pour extraire des champs spécifiques dans un fichier JSON, en particulier lors de la manipulation des informations d'identification.

3. **Sécurité** : L'utilisation de `jq` permet de transformer et manipuler les credentials sans les stocker dans des fichiers temporaires non sécurisés ou visibles dans les journaux de la CI/CD.

Voici un exemple d'utilisation dans le pipeline :
```bash
# Vérification et enregistrement du fichier de clé JSON avec jq
echo "$GOOGLE_CREDENTIALS" | jq '.' > /tmp/keyfile.json
```
Cette commande permet de convertir la variable d'environnement contenant les credentials JSON en un fichier temporaire sécurisé et correctement formaté.

---




### Commande pour exécuter tous les modèles dbt

Pour exécuter tous les modèles de transformations dbt, la commande suivante est utilisée dans la pipeline :

```bash
dbt run
```

### Commande pour exécuter un modèle spécifique

Pour exécuter un modèle particulier, par exemple le modèle `elimination_doublons.sql` :

```bash
dbt run --select elimination_doublons
```

## Tests dbt

Des tests automatiques sont définis pour garantir l’intégrité des données. Pour exécuter les tests dbt :

```bash
dbt test
```

## Documentation dbt

La documentation de dbt est générée automatiquement pour permettre une visualisation claire des modèles et des transformations.

### Génération de la documentation

Pour générer la documentation du projet dbt :

```bash
dbt docs generate
```

### Visualisation de la documentation

Une fois générée, la documentation peut être visualisée avec :

```bash
dbt docs serve
```

Cela ouvre un serveur local où la documentation est accessible via un navigateur.

---

## Auteur 
SERGES ADJOMO