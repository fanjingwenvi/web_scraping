import os
from dotenv import load_dotenv, find_dotenv 
from sqlalchemy import create_engine 
# import time 

def get_pgdatabase_keys():
    """
    Get the enviromental keys of the postgres database  Docker service  
    """
    load_dotenv(find_dotenv())
    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")
    host = os.environ.get('POSTGRES_HOST')
    port = os.environ.get('POSTGRES_PORT')
    database =  os.environ.get('POSTGRES_DB')
    return user, password, host, port, database

def create_pgdatabase_engine(): 
    """
    create the engine that can connect to the postgres database
    """
    user, password, host, port, database = get_pgdatabase_keys()
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    return engine

def save_data(df, engine, table_name, subcategory):
    """
    add the created and save data to the database  
    """
    # current_time = time.localtime()
    # df['created_at'] =  time.strftime("%Y-%m-%d %H:%M:%S", current_time)
    df['subcategory'] =  subcategory
    df.to_sql(name=table_name, con=engine, if_exists='append')