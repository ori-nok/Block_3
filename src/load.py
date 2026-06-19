import pandas as pd
from sqlalchemy import create_engine, text

def load_to_staging(clean_cust, clean_ord, clean_pay, clean_ev, clean_prod):
    # Настройки подключения
    db_user = 'postgres'
    db_password = '1'
    db_host = 'localhost'
    db_port = '5432'
    db_name = 'postgres'
    
    connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(connection_string)
    
    # Загрузка в Staging
    clean_cust.to_sql('stg_customers', con=engine, if_exists='replace', index=False)
    clean_ord.to_sql('stg_orders', con=engine, if_exists='replace', index=False)
    clean_pay.to_sql('stg_payments', con=engine, if_exists='replace', index=False)
    clean_ev.to_sql('stg_events', con=engine, if_exists='replace', index=False)
    clean_prod.to_sql('stg_products', con=engine, if_exists='replace', index=False)
    
    return engine

def create_dwh_and_load(engine):
    # Читаем DDL скрипт
    with open('ddl/dwh_schema.sql', 'r', encoding='utf-8') as f:
        ddl_script = f.read()
    
    # Выполняем DDL
    with engine.begin() as conn:
        for statement in ddl_script.split(';'):
            if statement.strip():
                conn.execute(text(statement))
    
    print("DWH-модель создана и наполнена данными")
    return engine
