
  
    

    create or replace table `e-datacap`.`ds_etl`.`banques_cleaned`
      
    
    

    OPTIONS()
    as (
      

SELECT DISTINCT
    Id,
    TRIM(UPPER(Name)) as name_standardized,
    TIMESTAMP(CreatedDate) as created_date_cleaned
FROM `e-datacap`.ds_etl.banques_test
    );
  