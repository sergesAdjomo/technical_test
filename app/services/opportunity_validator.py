# Chemin: app/services/opportunity_validator.py

import pandas as pd
from typing import Dict, List, Tuple

class OpportunityValidator:
    @staticmethod
    def validate_opportunity(data: Dict) -> Tuple[bool, List[str]]:
        problemes = []
        
        # Vérification des données obligatoires
        required_fields = {
            'Age_emprunteur__c': "Âge de l'emprunteur",
            'TotRev__c': "Revenu total",
            'BanquePrincipaleEmp__c': "Banque principale"
        }
        
        for field, name in required_fields.items():
            if field not in data or pd.isna(data[field]):
                problemes.append(f"{name} manquant")
        
        # Ajouter validation du format des montants
        if any(value < 0 for value in [data.get('MontPretPricip__c', 0), 
                                    data.get('MontAppPerso__c', 0)]):
            problemes.append("Les montants ne peuvent pas être négatifs")
            
        # Vérification de l'âge
        if 'Age_emprunteur__c' in data and not pd.isna(data['Age_emprunteur__c']):
            age = data['Age_emprunteur__c']
            if age < 18 or age > 85:
                problemes.append("L'âge doit être entre 18 et 85 ans")
                
        # Vérification du revenu
        if 'TotRev__c' in data and not pd.isna(data['TotRev__c']):
            revenu = data['TotRev__c']
            if revenu < 1000:
                problemes.append("Revenu insuffisant (minimum 1000€)")
                
        # Vérification du taux d'endettement
        if 'TxEndetApres__c' in data and not pd.isna(data['TxEndetApres__c']):
            taux = data['TxEndetApres__c']
            if taux > 35:
                problemes.append("Taux d'endettement trop élevé (> 35%)")
                
        # Vérification du statut
        if data.get('StageName') == '6-Perdue':
            problemes.append("Opportunité déjà perdue")


            
        return len(problemes) == 0, problemes