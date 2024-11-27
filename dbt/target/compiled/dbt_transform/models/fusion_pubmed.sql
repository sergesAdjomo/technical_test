

-- Fusionner les tables pubmed et pubmedjson
SELECT id, title, date, journal
FROM `e-datacap`.`ds_etl`.`pubmed`

UNION ALL

SELECT id, title, date, journal
FROM `e-datacap`.`ds_etl`.`pubmedjson`

ORDER BY id