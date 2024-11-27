# check_data.py
import pandas as pd
import os

def check_data():
    data_path = "data_sources/gold"
    
    # Vérifier si les fichiers existent
    opps_path = os.path.join(data_path, "opportunities_cleaned.csv")
    props_path = os.path.join(data_path, "propositions_cleaned.csv")
    
    print(f"Vérification des chemins:")
    print(f"Opportunities: {opps_path} - Existe: {os.path.exists(opps_path)}")
    print(f"Propositions: {props_path} - Existe: {os.path.exists(props_path)}")
    
    if os.path.exists(opps_path) and os.path.exists(props_path):
        # Lire et afficher les données
        opps = pd.read_csv(opps_path)
        props = pd.read_csv(props_path)
        
        print("\nDonnées des opportunités:")
        print(opps)
        print("\nDonnées des propositions:")
        print(props)
    else:
        print("\nCréation des données de test...")
        # Créer le dossier si nécessaire
        os.makedirs(data_path, exist_ok=True)
        
        # Créer les données de test
        opportunities = pd.DataFrame({
            'id': ['123', '456'],
            'age': [30, 45],
            'revenu_total': [50000, 75000],
            'banque_principale': ['BNP', 'SG']
        })
        
        propositions = pd.DataFrame({
            'opportunity_id': ['123', '123', '456'],
            'montant': [100000, 150000, 200000],
            'taux': [2.5, 2.7, 2.9],
            'duree': [240, 300, 360],
            'mensualite': [500, 600, 700]
        })
        
        # Sauvegarder les données
        opportunities.to_csv(opps_path, index=False)
        propositions.to_csv(props_path, index=False)
        print("Données de test créées!")

if __name__ == "__main__":
    check_data()