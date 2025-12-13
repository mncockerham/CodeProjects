{{ config(materialized='table') }}

select * from postgres_scan('{{ var("source_url") }}', 'postgres_air', 'phone')
