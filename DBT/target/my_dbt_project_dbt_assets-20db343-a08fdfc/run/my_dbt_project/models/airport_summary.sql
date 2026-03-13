
  
    
    

    create  table
      "local"."main"."airport_summary__dbt_tmp"
  
    as (
      

SELECT 
    iso_country, 
    count(distinct city) as unique_city_count
FROM raw_airport
GROUP BY 1
    );
  
  