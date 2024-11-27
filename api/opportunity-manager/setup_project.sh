#!/bin/bash

# Nom du projet
PROJECT_NAME="opportunity_manager"

# Fonction pour créer un fichier avec du contenu
create_file() {
    local file_path="$1"
    local content="$2"
    echo -e "$content" > "$file_path"
    echo "Créé: $file_path"
}

# Création de l'arborescence principale
mkdir -p "$PROJECT_NAME"/{app/{routes,services,models,templates},data_sources/gold,static,tests}

# Création des fichiers Python vides avec __init__.py
touch "$PROJECT_NAME/app/__init__.py"
touch "$PROJECT_NAME/app/routes/__init__.py"
touch "$PROJECT_NAME/app/services/__init__.py"
touch "$PROJECT_NAME/app/models/__init__.py"
touch "$PROJECT_NAME/tests/__init__.py"

# Création du fichier requirements.txt
create_file "$PROJECT_NAME/requirements.txt" "fastapi==0.104.1\nuvicorn==0.24.0\npandas==2.1.3\npydantic==2.5.2\nopenpyxl==3.1.2\npython-multipart==0.0.6\njinja2==3.1.2"

# Création du fichier README.md
create_file "$PROJECT_NAME/README.md" "# Gestionnaire d'Opportunités

## Description
Application de gestion des opportunités commerciales avec FastAPI.

## Installation
1. Créer un environnement virtuel :
   \`\`\`bash
   python -m venv venv
   \`\`\`

2. Activer l'environnement virtuel :
   - Windows : \`venv\\Scripts\\activate\`
   - Linux/MacOS : \`source venv/bin/activate\`

3. Installer les dépendances :
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

## Lancement
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

## Documentation API
Accéder à \`http://localhost:8000/docs\` après le lancement."

# Création du fichier .env
create_file "$PROJECT_NAME/.env" "# Configuration de l'environnement
DATA_PATH=data_sources/gold
PORT=8000
HOST=0.0.0.0"

# Création du fichier Dockerfile
create_file "$PROJECT_NAME/Dockerfile" "FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]"

# Création du fichier .gitignore
create_file "$PROJECT_NAME/.gitignore" "# Python
__pycache__/
*.py[cod]
*$py.class
.Python
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environnement
.env

# Data
*.csv
*.xlsx
*.xls

# Système
.DS_Store
Thumbs.db"

# Création du fichier style.css
create_file "$PROJECT_NAME/static/style.css" "/* Style de base */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f5f5f5;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
    color: #333;
    margin-bottom: 20px;
}

.form-group {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 5px;
    color: #666;
}

input[type=\"text\"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}"

# Création du fichier index.html
create_file "$PROJECT_NAME/app/templates/index.html" "<!DOCTYPE html>
<html lang=\"fr\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Gestionnaire d'Opportunités</title>
    <link rel=\"stylesheet\" href=\"/static/style.css\">
</head>
<body>
    <div class=\"container\">
        <h1>Recherche d'Opportunité</h1>
        <div class=\"form-group\">
            <form action=\"/opportunities\" method=\"get\">
                <label for=\"opportunity_id\">ID de l'Opportunité:</label>
                <input type=\"text\" id=\"opportunity_id\" name=\"opportunity_id\" required>
                <button type=\"submit\">Rechercher</button>
            </form>
        </div>
    </div>
</body>
</html>"

echo "Structure du projet créée avec succès dans le dossier $PROJECT_NAME!"
echo "Pour démarrer le projet:"
echo "1. cd $PROJECT_NAME"
echo "2. python -m venv venv"
echo "3. source venv/bin/activate (Linux/MacOS) ou .\\venv\\Scripts\\activate (Windows)"
echo "4. pip install -r requirements.txt"
echo "5. uvicorn app.main:app --reload"