

WITH cleaned_propositions AS (
    SELECT *,
        (CAST(TXHA__c AS FLOAT64) / 100) * DureePret_Mois__c as total_cost
    FROM `e-datacap`.ds_etl.propositions_test
    WHERE Etape_Source__c NOT LIKE '%Non éligible%'
    AND Opportunity__c IN (
        SELECT Id FROM `e-datacap`.`ds_etl`.`opportunity_cleaned`
    )
)
SELECT 
    Id,
    Opportunity__c,
    DureePret_Mois__c,
    TXHA__c,
    total_cost,
    Etape_Source__c,
    TIMESTAMP(CreatedDate) as created_date_cleaned
FROM cleaned_propositions