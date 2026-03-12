{{ config(materialized='table') }}

SELECT 
    iso_country, 
    count(distinct city) as unique_city_count
FROM raw_airport
GROUP BY 1
