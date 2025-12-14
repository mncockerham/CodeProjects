
  
    
    

    create  table
      "local"."main"."phone_ppi_clean__dbt_tmp"
  
    as (
      

select 
    phone_id,
    account_id,
    sha256(phone) as phone_encrypted,
    phone_type,
    primary_phone,
    update_ts
from postgres_scan('postgresql://postgres:ZAQ!2wsx@localhost:5432/postgres_air', 'postgres_air', 'phone')
    );
  
  