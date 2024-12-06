# Guide de déploiement manuel sur Google Cloud Platform (GCP)

Ce guide décrit le processus de déploiement manuel d'une application Docker sur Google Cloud Platform en utilisant Artifact Registry et Cloud Run.

## Prérequis

- Google Cloud SDK installé localement
- Docker Desktop installé et en cours d'exécution
- Un projet GCP actif avec facturation activée
- Les APIs nécessaires activées dans GCP :
  - Artifact Registry API
  - Cloud Run API

## 1. Configuration initiale

### 1.1 Vérification de la configuration GCP
```bash
# Vérifier le projet actif
gcloud config get-value project

# Configurer le projet si nécessaire
gcloud config set project [VOTRE_PROJECT_ID]

# Configurer la région
gcloud config set compute/region [VOTRE_REGION]
```

### 1.2 Configuration de Docker pour GCP
```bash
# Configurer l'authentification Docker pour Artifact Registry
gcloud auth configure-docker [REGION]-docker.pkg.dev
```
Cette commande met à jour le fichier `config.json` de Docker pour permettre l'authentification avec GCP.
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
## 2. Création du Repository dans Artifact Registry

```bash
# Créer un nouveau repository
gcloud artifacts repositories create [REPO_NAME] \
    --repository-format=docker \
    --location=[REGION] \
    --description="Description de votre repository"

# Vérifier la création
gcloud artifacts repositories list
```

## 3. Construction et Push de l'Image

### 3.1 Construction de l'image Docker
```bash
# Construire l'image localement
docker build -t [NOM_APPLICATION] .
docker build -t opportunity-manager .
```

### 3.2 Tagging et Push de l'image
```bash
# Tagger l'image pour Artifact Registry
docker tag [NOM_APPLICATION] [REGION]-docker.pkg.dev/[PROJECT_ID]/[REPO_NAME]/[IMAGE_NAME]:[TAG]

# Pousser l'image vers Artifact Registry
docker push [REGION]-docker.pkg.dev/[PROJECT_ID]/[REPO_NAME]/[IMAGE_NAME]:[TAG]
```

Exemple concret :
```bash
docker tag opportunity_manager us-central1-docker.pkg.dev/e-datacap/opportunity-manager/app:v1

docker push us-central1-docker.pkg.dev/e-datacap/opportunity-manager/app:v1
```

## 4. Déploiement sur Cloud Run

```bash
gcloud run deploy [SERVICE_NAME] \
  --image=[REGION]-docker.pkg.dev/[PROJECT_ID]/[REPO_NAME]/[IMAGE_NAME]:[TAG] \
  --platform managed \
  --region=[REGION] \
  --allow-unauthenticated
```

Exemple :
```bash
gcloud run deploy opportunity-manager \
  --image=us-central1-docker.pkg.dev/e-datacap/opportunity-manager/app:v1 \
  --platform managed \
  --region=us-central1 \
  --allow-unauthenticated
```

## 5. Vérification du déploiement

Une fois le déploiement terminé, Cloud Run fournira une URL où votre application est accessible. Vous pouvez vérifier le statut de votre service avec :

```bash
gcloud run services describe [SERVICE_NAME] --region=[REGION]
```
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------

## 6. Commande pour deployé dbt en local.


```bash
dbt init dbt_transform
dbt debug
dbt run  
```


## 7. Commande pour deployé l'infra en local.

```bash
terraform init -reconfigure
terraform plan -var-file="env\dev.tfvars"

terraform apply -var-file="env\dev.tfvars"
```















## Notes importantes

- Les images poussées vers Artifact Registry sont immuables. Une fois poussée, une image avec un tag spécifique ne peut pas être modifiée.
- Utilisez des tags significatifs pour vos images (ex: v1, v1.0.0, latest).
- L'option `--allow-unauthenticated` rend votre service accessible publiquement. Retirez cette option si vous souhaitez restreindre l'accès.

## Dépannage courant

1. **Erreur "Repository not found"**
   - Solution : Créer d'abord le repository dans Artifact Registry

2. **Erreur d'authentification Docker**
   - Solution : Réexécuter `gcloud auth configure-docker`

3. **Erreur de push**
   - Vérifier que le repository existe
   - Vérifier les permissions IAM
   - Vérifier le format du tag de l'image

## Ressources supplémentaires

- [Documentation Artifact Registry](https://cloud.google.com/artifact-registry/docs)
- [Documentation Cloud Run](https://cloud.google.com/run/docs)
- [Meilleures pratiques Docker](https://cloud.google.com/architecture/best-practices-for-building-containers)
