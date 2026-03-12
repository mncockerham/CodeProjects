

select 
    phone_id,
    account_id,
    sha256(phone) as phone_encrypted,
    phone_type,
    primary_phone,
    update_ts
from postgres_scan('postgresql://postgres@localhost:5432/postgres_air', 'postgres_air', 'phone')