# tests/test_opportunity_service.py
import pytest
from app.services.opportunity_service import OpportunityInfoService
import pandas as pd
import os

class TestOpportunityInfoService:
    @pytest.fixture
    def service(self, tmp_path):
        """Créer un service de test avec des données fictives"""
        # Créer des données de test
        opportunities_data = {
            'id': ['123', '456'],
            'age': [30, 45],
            'revenu_total': [50000, 75000],
            'banque_principale': ['BNP', 'SG']
        }
        
        propositions_data = {
            'opportunity_id': ['123', '123'],
            'montant': [100000, 150000],
            'taux': [2.5, 2.7],
            'duree': [240, 300],
            'mensualite': [500, 600]
        }
        
        # Créer les fichiers CSV temporaires
        data_path = tmp_path / "data"
        os.makedirs(data_path)
        
        pd.DataFrame(opportunities_data).to_csv(data_path / "opportunities_cleaned.csv", index=False)
        pd.DataFrame(propositions_data).to_csv(data_path / "propositions_cleaned.csv", index=False)
        
        return OpportunityInfoService(str(data_path))

    def test_get_info_valid_opportunity(self, service):
        """Tester la récupération d'une opportunité valide"""
        info = service.get_info("123")
        assert info['est_exploitable'] == True
        assert info['client']['age'] == 30
        assert info['client']['revenu_total'] == 50000
        assert info['client']['banque_principale'] == 'BNP'
        assert 'propositions' not in info

    def test_get_info_with_propositions(self, service):
        """Tester la récupération d'une opportunité avec ses propositions"""
        info = service.get_info("123", include_propositions=True)
        assert info['est_exploitable'] == True
        assert len(info['propositions']) == 2
        assert info['propositions'][0]['montant'] == 100000

    def test_get_info_invalid_opportunity(self, service):
        """Tester la récupération d'une opportunité inexistante"""
        info = service.get_info("999")
        assert info['est_exploitable'] == False
        assert "Opportunité non trouvée" in info['raisons_non_exploitable']
        
    # Tester les cas limites
    def test_edge_cases():
         assert validate_opportunity({'Age_emprunteur__c': 18}) == (False, ["Revenu total manquant"])
         assert validate_opportunity({'Age_emprunteur__c': 85}) == (False, ["Revenu total manquant"])
        
    def test_to_excel(self, service, tmp_path):
        """Tester l'export Excel d'une opportunité"""
        output_path = str(tmp_path / "test_export.xlsx")
        success = service.to_excel("123", output_path)
    
        assert success == True
        assert os.path.exists(output_path)
        
        # Vérifier le contenu du fichier Excel
        xl = pd.read_excel(output_path, sheet_name=None)
        assert 'Client' in xl
        assert 'Propositions' in xl