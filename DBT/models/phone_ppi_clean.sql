{{ config(materialized='table') }}

select 
    phone_id,
    account_id,
    sha256(phone) as phone_encrypted,
    phone_type,
    primary_phone,
    update_ts
from postgres_scan('{{ var("source_url") }}', 'postgres_air', 'phone')
