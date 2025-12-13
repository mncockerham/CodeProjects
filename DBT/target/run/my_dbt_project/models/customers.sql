
  
    
    

    create  table
      "local"."main"."customers__dbt_tmp"
  
    as (
      

select * from postgres_scan('postgresql://postgres:ZAQ!2wsx@localhost:5432/postgres', 'public', 'customer')
    );
  
  