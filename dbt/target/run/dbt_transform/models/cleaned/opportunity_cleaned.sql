
  
    

    create or replace table `e-datacap`.`ds_etl`.`opportunity_cleaned`
      
    
    

    OPTIONS()
    as (
      

WITH cleaned_opportunities AS (
    SELECT *,
        CASE 
            WHEN TotRev__c > 0 
            AND Age_emprunteur__c >= 18 
            AND Age_emprunteur__c <= 80 
            THEN TRUE 
            ELSE FALSE 
        END as is_exploitable,
        TIMESTAMP(CreatedDate) as created_date_cleaned
    FROM `e-datacap`.ds_etl.opportunity_test
    WHERE TotRev__c > 0 
    AND Age_emprunteur__c >= 18 
    AND Age_emprunteur__c <= 80
)
SELECT 
    Id,
    Age_emprunteur__c,
    TotRev__c,
    BanquePrincipaleEmp__c,
    created_date_cleaned,
    is_exploitable,
    StageName,
    TxEndetApres__c,
    TypBien__c,
    TypProj__c,
    UsagBien__c
FROM cleaned_opportunities
    );
  