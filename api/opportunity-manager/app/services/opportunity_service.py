# app/services/opportunity_service.py
import os
import pandas as pd
from typing import Dict, Optional, List
from google.cloud import bigquery
import logging
from pathlib import Path
from .opportunity_validator import OpportunityValidator
import db_dtypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpportunityInfoService:
    # Ajouter le client bigquery en paramètre de la fonction __init__
    # Ajouter le client bigquery en paramètre de la fonction get_info 
    def get_info(self, opportunity_id: str, include_propositions: bool = False) -> Dict:
        """Récupère les informations d'une opportunité."""
        logger.info(f"Recherche de l'opportunité {opportunity_id}")
        project_id = os.environ.get('PROJECT_ID', 'PROJECT_ID env var is not set.')
        dataset = os.environ.get('DATASET', 'DATASET env var is not set.')

        bigquery_client = bigquery.Client(project=project_id)
        
        # Filtrer les opportunités sans utiliser d'index
        # select * from opportunities where Id = opportunity_id Executer la requete suivante avec le client bigquery
       
    
        sql = f"""
            SELECT *
            FROM `{project_id}.{dataset}.opportunity_cleaned`
            WHERE Id = '{opportunity_id}';
        """
        # Start the query, passing in the extra
        query_job = bigquery_client.query_and_wait(
            sql,    # Location must match that of the dataset(s) referenced in the query# and of the destination table.    location="US",
        )  # API request - starts the query

        opportunity = query_job.to_dataframe()

        if len(opportunity) == 0:
            return {
                'informations_principales': None,
                'est_exploitable': False,
                'raisons_non_exploitable': ["Opportunité non trouvée"],
                'details_complementaires': None,
                'propositions': None
            }
        print(f"number opportunity treive = {len(opportunity)}")
        opportunity_data = opportunity.iloc[0].to_dict()
        validator = OpportunityValidator()
        est_exploitable, problemes = validator.validate_opportunity(opportunity_data)
        
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
        
        print(f"response = {response}")
        # Ajouter les propositions si demandées et si l'opportunité est exploitable
        if include_propositions:
            sql = f"""
                SELECT *
                FROM `{project_id}.{dataset}.propositions_cleaned`
                WHERE Id = '{opportunity_id}';
                """
            # Start the query, passing in the extra
            query_job = bigquery_client.query_and_wait(
                sql,    # Location must match that of the dataset(s) referenced in the query# and of the destination table.    location="US",
            )  # API request - starts the query
            
            propositions = query_job.to_dataframe()
            print(f"propositions = {propositions}")
            print(f"taille de proposition {len(propositions)}")
            if len(propositions) > 0:
                response['propositions'] = [{
                    'taux': prop.get('TXHA__c'),
                    'duree_mois': prop.get('DureePret_Mois__c'),
                    'etape': prop.get('Etape_Source__c')
                } for prop in propositions]
                
      #       logger.info(f"Ajout de {len(propositions) if propositions else 0} propositions")
        
        return response

    def search_opportunities(
        self,
        age_min: int,
        age_max: int,
        revenu_min: float,
        banque: str,
        limit: int 
    ) -> List[Dict]:
        """Recherche des opportunités selon les critères."""
        logger.info(f"Recherche avancée - Critères: age_min={age_min}, age_max={age_max}, revenu_min={revenu_min}, banque={banque}")
        try: 
            project_id = os.environ.get('PROJECT_ID', 'PROJECT_ID env var is not set.')
            dataset = os.environ.get('DATASET', 'DATASET env var is not set.')
            bigquery_client = bigquery.Client(project=project_id)

            sql = f"""
                SELECT *
                FROM `{project_id}.{dataset}.opportunity_cleaned`
                WHERE Age_emprunteur__c >= {age_min} and Age_emprunteur__c <= {age_max} and CAST(TotRev__c AS INT64) >= CAST( {revenu_min} AS INT64) and BanquePrincipaleEmp__c = '{banque}';
                """
            # Start the query, passing in the extra
            query_job = bigquery_client.query_and_wait(
                sql,    # Location must match that of the dataset(s) referenced in the query# and of the destination table.    location="US",
            )  # API request - starts the query
            
            filtered_df = query_job.to_dataframe()
            print(f"filtered_df = {filtered_df}")
            print(f"taille de filtered_df {len(filtered_df)}")
            
            filtered_df = filtered_df.head(limit)
            
            results = []

            for _, row in filtered_df.iterrows():
                opportunity_data = row.to_dict()
                est_exploitable, problemes = OpportunityValidator().validate_opportunity(opportunity_data)
                
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