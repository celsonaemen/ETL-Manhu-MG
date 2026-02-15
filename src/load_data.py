from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

possiveis_caminhos = [
    Path(__file__).resolve().parent.parent / '.env',
    Path('/opt/airflow/.env'),
]
env_path = None
for caminho in possiveis_caminhos:
    if caminho.exists():
        env_path = caminho
        break
if env_path:
    load_dotenv(env_path)
    logger.info(f'Arquivo .env carregado de: {env_path}')

DB_USER = os.getenv('DB_USER', 'angeldarkblue')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123')
DB_NAME = os.getenv('DB_NAME', 'weather_warehouse')
DB_HOST = os.getenv('DB_HOST', 'weather-postgres')
DB_PORT = os.getenv('DB_PORT', '5432')
logger.info(f'Configurações do banco: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def get_engine():
    password_encoded = quote_plus(DB_PASSWORD)
    connection_string = f'postgresql+psycopg2://{DB_USER}:{password_encoded}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    return create_engine(connection_string)

def create_table_if_not_exists(engine):
    """Cria a tabela se não existir (Versão com todas as colunas do DataFrame)"""
    create_table_sql = text('''
    CREATE TABLE IF NOT EXISTS climate_records (
        id SERIAL PRIMARY KEY,
        base VARCHAR(50),
        visibility INTEGER,
        dt TIMESTAMP WITH TIME ZONE,
        timezone INTEGER,
        city_id INTEGER,
        city_name VARCHAR(100),
        code INTEGER,
        longitude FLOAT,
        latitude FLOAT,
        temperature FLOAT,
        feels_like FLOAT,
        temp_min FLOAT,
        temp_max FLOAT,
        pressure INTEGER,
        humidity INTEGER,
        sea_level INTEGER,
        grnd_level INTEGER,
        wind_speed FLOAT,
        wind_deg INTEGER,
        wind_gust FLOAT,
        clouds INTEGER,
        sys_id INTEGER,
        country VARCHAR(10),
        sunrise TIMESTAMP WITH TIME ZONE,
        sunset TIMESTAMP WITH TIME ZONE,
        weather_id INTEGER,
        weather_main VARCHAR(50),
        weather_description VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    
    try:
        with engine.begin() as conn:
            conn.execute(create_table_sql)
        logger.info('Tabela climate_records verificada/criada com sucesso')
    except Exception as e:
        logger.error(f'Erro ao criar tabela: {e}')
        raise

def load_data(table_name: str, df: pd.DataFrame, engine):
    logger.info(f'Carregando {len(df)} registros na tabela {table_name}...')
    try:
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        logger.info('Dados carregados com sucesso!')
    except Exception as e:
        logger.error(f'Erro ao carregar dados: {e}')
        raise

def check_data(table_name: str, engine):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f'SELECT COUNT(*) FROM {table_name}')).fetchone()
            total = result[0] if result else 0
        logger.info(f'Total de registros na tabela {table_name}: {total}')
        return total
    except Exception as e:
        logger.error(f'Erro ao verificar dados: {e}')
        return 0

def load_pipeline(df: pd.DataFrame, table_name: str = 'climate_records'):
    logger.info('\n' + '='*50)
    logger.info('Iniciando carga de dados no banco...')
    logger.info('='*50)
    
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        logger.info('Conexão com o banco de dados estabelecida com sucesso')
        
        create_table_if_not_exists(engine)
        load_data(table_name, df, engine)
        total = check_data(table_name, engine)
        
        logger.info('\n' + '='*50)
        logger.info('Carga de dados concluída com sucesso!')
        logger.info(f'Total de registros na tabela: {total}')
        logger.info('='*50)
        return True
        
    except Exception as e:
        logger.error(f'Erro no pipeline de carga: {e}')
        raise

if __name__ == '__main__':
    from transform_data import data_transformation
    df = data_transformation()
    load_pipeline(df)
