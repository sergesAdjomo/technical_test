{{ config(materialized='table') }}

SELECT DISTINCT
    Id,
    TRIM(UPPER(Name)) as name_standardized,
    TIMESTAMP(CreatedDate) as created_date_cleaned
FROM {{ source('ds_etl', 'banques_test') }}