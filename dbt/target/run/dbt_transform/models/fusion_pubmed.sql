
  
    

    create or replace table `e-datacap`.`ds_etl`.`fusion_pubmed`
      
    
    

    OPTIONS()
    as (
      

-- Fusionner les tables pubmed et pubmedjson
SELECT id, title, date, journal
FROM `e-datacap`.`ds_etl`.`pubmed`

UNION ALL

SELECT id, title, date, journal
FROM `e-datacap`.`ds_etl`.`pubmedjson`

ORDER BY id
    );
  