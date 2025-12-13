
  
    
    

    create  table
      "local"."main"."phone__dbt_tmp"
  
    as (
      

select * from postgres_scan('postgresql://postgres:ZAQ!2wsx@localhost:5432/postgres_air', 'postgres_air', 'phone')
    );
  
  