

SELECT DISTINCT
    Id,
    TRIM(UPPER(Name)) as name_standardized,
    TIMESTAMP(CreatedDate) as created_date_cleaned
FROM `e-datacap`.ds_etl.banques_test