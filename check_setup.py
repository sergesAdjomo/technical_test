# check_setup.py
import os
from pathlib import Path

def check_structure():
    base_path = Path.cwd()
    print(f"Chemin de base: {base_path}")
    
    # Structure attendue
    expected_structure = {
        "app": {
            "__init__.py": True,
            "main.py": True,
            "models": {
                "__init__.py": True,
                "opportunity.py": True
            },
            "routes": {
                "__init__.py": True,
                "opportunities.py": True,
                "health.py": True
            },
            "services": {
                "__init__.py": True,
                "opportunity_service.py": True,
                "opportunity_validator.py": True
            },
            "templates": {
                "index.html": True
            }
        },
        "static": {
            "style.css": True
        },
        "data_sources": {
            "gold": {
                "opportunities_cleaned.csv": True,
                "propositions_cleaned.csv": True
            }
        }
    }
    
    def check_directory(structure, current_path):
        for name, content in structure.items():
            path = current_path / name
            if isinstance(content, dict):
                if not path.exists():
                    print(f"❌ Dossier manquant: {path}")
                    if "gold" in str(path):  # Créer automatiquement le dossier data
                        path.mkdir(parents=True, exist_ok=True)
                        print(f"✅ Dossier créé: {path}")
                else:
                    print(f"✅ Dossier trouvé: {path}")
                check_directory(content, path)
            else:
                if not path.exists():
                    print(f"❌ Fichier manquant: {path}")
                else:
                    print(f"✅ Fichier trouvé: {path}")
    
    check_directory(expected_structure, base_path)

if __name__ == "__main__":
    check_structure()