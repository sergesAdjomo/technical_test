# app/services/opportunity_service.py
import pandas as pd
from typing import Dict, Optional, List
import logging
from pathlib import Path
from .opportunity_validator import OpportunityValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpportunityInfoService:
    def __init__(self, data_path: str):
        """Initialise le service avec le chemin vers les données."""
        self.data_path = data_path
        logger.info(f"Initialisation du service avec data_path: {data_path}")
        
        opps_path = Path(data_path) / "opportunities_cleaned.csv"
        props_path = Path(data_path) / "propositions_cleaned.csv"
        
        if not opps_path.exists() or not props_path.exists():
            raise FileNotFoundError(f"Fichiers de données manquants dans {data_path}")
            
        try:
            # Charger les données sans définir d'index
            self.opportunities_df = pd.read_csv(opps_path)
            self.propositions_df = pd.read_csv(props_path)
            logger.info(f"Données chargées - Opportunités: {len(self.opportunities_df)}, Propositions: {len(self.propositions_df)}")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données: {str(e)}")
            raise
            
        self.validator = OpportunityValidator()

    def get_info(self, opportunity_id: str, include_propositions: bool = False) -> Dict:
        """Récupère les informations d'une opportunité."""
        logger.info(f"Recherche de l'opportunité {opportunity_id}")
        
        # Filtrer les opportunités sans utiliser d'index
        opportunity = self.opportunities_df[self.opportunities_df['Id'] == opportunity_id]
        
        if len(opportunity) == 0:
            return {
                'informations_principales': None,
                'est_exploitable': False,
                'raisons_non_exploitable': ["Opportunité non trouvée"],
                'details_complementaires': None,
                'propositions': None
            }
        
        opportunity_data = opportunity.iloc[0].to_dict()
        est_exploitable, problemes = self.validator.validate_opportunity(opportunity_data)
        
        # Construire la réponse
        response = {
            'id': opportunity_id,
            'informations_principales': {
                'age': opportunity_data.get('Age_emprunteur__c'),
                'revenu_mensuel': opportunity_data.get('TotRev__c'),
                'banque': opportunity_data.get('BanquePrincipaleEmp__c')
            },
            'est_exploitable': est_exploitable,
            'raisons_non_exploitable': problemes if not est_exploitable else None,
            'details_complementaires': {
                'type_bien': opportunity_data.get('TypBien__c'),
                'usage_bien': opportunity_data.get('UsagBien__c'),
                'type_projet': opportunity_data.get('TypProj__c'),
                'montant_projet': {
                    'pret_principal': opportunity_data.get('MontPretPricip__c'),
                    'apport_personnel': opportunity_data.get('MontAppPerso__c'),
                    'travaux': opportunity_data.get('MontEstimTravaux__c')
                },
                'situation': {
                    'actuelle': opportunity_data.get('SituActu__c'),
                    'taux_endettement': opportunity_data.get('TxEndetApres__c'),
                    'charges_mensuelles': opportunity_data.get('TotCharges__c')
                }
            },
            'propositions': None
        }
        
        # Ajouter les propositions si demandées et si l'opportunité est exploitable
        if include_propositions:
            propositions = self.propositions_df[
                self.propositions_df['Opportunity__c'] == opportunity_id
            ].to_dict('records')
            
            if propositions:
                response['propositions'] = [{
                    'taux': prop.get('TXHA__c'),
                    'duree_mois': prop.get('DureePret_Mois__c'),
                    'etape': prop.get('Etape_Source__c')
                } for prop in propositions]
                
            logger.info(f"Ajout de {len(propositions) if propositions else 0} propositions")
        
        return response

    def search_opportunities(
        self,
        age_min: Optional[int] = None,
        age_max: Optional[int] = None,
        revenu_min: Optional[float] = None,
        banque: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """Recherche des opportunités selon les critères."""
        try:
            filtered_df = self.opportunities_df.copy()
            
            if age_min is not None:
                filtered_df = filtered_df[filtered_df['Age_emprunteur__c'] >= age_min]
            if age_max is not None:
                filtered_df = filtered_df[filtered_df['Age_emprunteur__c'] <= age_max]
            if revenu_min is not None:
                filtered_df = filtered_df[filtered_df['TotRev__c'] >= revenu_min]
            if banque:
                filtered_df = filtered_df[filtered_df['BanquePrincipaleEmp__c'] == banque]
            
            filtered_df = filtered_df.head(limit)
            
            results = []
            for _, row in filtered_df.iterrows():
                opportunity_data = row.to_dict()
                est_exploitable, problemes = self.validator.validate_opportunity(opportunity_data)
                
                result = {
                    'id': opportunity_data['Id'],
                    'informations_principales': {
                        'age': opportunity_data.get('Age_emprunteur__c'),
                        'revenu_mensuel': opportunity_data.get('TotRev__c'),
                        'banque': opportunity_data.get('BanquePrincipaleEmp__c')
                    },
                    'est_exploitable': est_exploitable,
                    'raisons_non_exploitable': problemes if not est_exploitable else None
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors de la recherche: {str(e)}")
            raise

    def to_excel(self, opportunity_id: str, output_path: str) -> bool:
        """Exporte les informations d'une opportunité vers un fichier Excel."""
        try:
            # Récupérer les informations de l'opportunité
            opportunity_info = self.get_info(opportunity_id, include_propositions=True)
            
            # Créer un writer Excel avec openpyxl
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Informations principales
                main_info = {
                    'Informations': [{
                        'Age': opportunity_info['informations_principales'].get('age'),
                        'Revenu mensuel': opportunity_info['informations_principales'].get('revenu_mensuel'),
                        'Banque': opportunity_info['informations_principales'].get('banque'),
                        'Est exploitable': opportunity_info['est_exploitable']
                    }]
                }
                pd.DataFrame(main_info['Informations']).to_excel(writer, sheet_name='Informations', index=False)
                
                # Détails complémentaires
                if opportunity_info.get('details_complementaires'):
                    details = opportunity_info['details_complementaires']
                    details_df = pd.DataFrame([{
                        'Type de bien': details.get('type_bien'),
                        'Usage du bien': details.get('usage_bien'),
                        'Type de projet': details.get('type_projet')
                    }])
                    details_df.to_excel(writer, sheet_name='Détails', index=False)
                
                # Propositions
                if opportunity_info.get('propositions'):
                    props_df = pd.DataFrame(opportunity_info['propositions'])
                    props_df.to_excel(writer, sheet_name='Propositions', index=False)
                
                # Raisons si non exploitable
                if not opportunity_info['est_exploitable'] and opportunity_info.get('raisons_non_exploitable'):
                    raisons_df = pd.DataFrame({'Raisons': opportunity_info['raisons_non_exploitable']})
                    raisons_df.to_excel(writer, sheet_name='Raisons', index=False)
            
            logger.info(f"Export Excel créé avec succès pour l'opportunité {opportunity_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'export Excel: {str(e)}")
            return False