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
    Path(__file__).resolve().parent.parent / 'config/.env',
    Path('/opt/airflow/.env'),
]

env_path = None
for caminho in possiveis_caminhos:
    if caminho.exists():
        env_path = caminho
        break

if env_path:
    load_dotenv(env_path)
    logger.info(f"Arquivo .env carregado de: {env_path}")
else:
    logger.warning("Arquivo .env não encontrado. Usando valores padrão ou variáveis de ambiente.")

DB_USER = os.getenv('DB_USER', 'angeldarkblue')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123')
DB_NAME = os.getenv('DB_NAME', 'weather_warehouse')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

logger.info(f"Configurações do banco: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def get_engine():
    """Cria conexão com o banco de dados"""
    password_encoded = quote_plus(DB_PASSWORD)
    connection_string = f"postgresql+psycopg2://{DB_USER}:{password_encoded}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    logger.info(f"Conectando em: {DB_HOST}:{DB_PORT}/{DB_NAME}")
    return create_engine(connection_string)

def create_table_if_not_exists(engine):
    """Cria a tabela se não existir"""
    create_table_sql = text("""
    CREATE TABLE IF NOT EXISTS climate_records (
        id SERIAL PRIMARY KEY,
        city_name VARCHAR(100),
        longitude FLOAT,
        latitude FLOAT,
        temperature FLOAT,
        feels_like FLOAT,
        temp_min FLOAT,
        temp_max FLOAT,
        pressure INTEGER,
        humidity INTEGER,
        wind_speed FLOAT,
        wind_deg INTEGER,
        clouds INTEGER,
        weather_main VARCHAR(50),
        weather_description VARCHAR(100),
        dt TIMESTAMP WITH TIME ZONE,
        sunrise TIMESTAMP WITH TIME ZONE,
        sunset TIMESTAMP WITH TIME ZONE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    try:
        with engine.connect() as conn:
            conn.execute(create_table_sql)
            conn.commit()
        logger.info("Tabela 'climate_records' verificada/criada com sucesso")
    except Exception as e:
        logger.error(f"Erro ao criar tabela: {e}")
        raise

def load_data(table_name: str, df: pd.DataFrame, engine):
    """Carrega dados no banco de dados"""
    logger.info(f"Carregando {len(df)} registros na tabela '{table_name}'...")
    
    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',
            index=False
        )
        logger.info(f"Dados carregados com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {e}")
        raise

def check_data(table_name: str, engine):
    """Verifica dados na tabela"""
    try:
        with engine.connect() as conn:
            query = text(f"SELECT COUNT(*) as total FROM {table_name}")
            result = conn.execute(query).fetchone()
            total = result[0] if result else 0
        
        logger.info(f"Total de registros na tabela '{table_name}': {total}")
        
        if total > 0:
            query_sample = text(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 5")
            df_sample = pd.read_sql_query(query_sample, con=engine)
            logger.info("\nÚltimos 5 registros:")
            print(df_sample.to_string())
        
        return total
    except Exception as e:
        logger.error(f"Erro ao verificar dados: {e}")
        return 0

def load_pipeline(df: pd.DataFrame, table_name: str = 'climate_records'):
    """Pipeline completo de carga de dados"""
    logger.info("\n" + "="*50)
    logger.info("Iniciando carga de dados no banco...")
    logger.info("="*50)
    
    try:
        engine = get_engine()
        
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Conexão com o banco de dados estabelecida com sucesso")
        
        create_table_if_not_exists(engine)
        
        load_data(table_name, df, engine)
        
        total = check_data(table_name, engine)
        
        logger.info("\n" + "="*50)
        logger.info("Carga de dados concluída com sucesso!")
        logger.info(f"Total de registros na tabela: {total}")
        logger.info("="*50)
        
        return True
        
    except Exception as e:
        logger.error(f"Erro no pipeline de carga: {e}")
        raise

if __name__ == "__main__":
    logger.info("Testando módulo de carga...")
    from transform_data import data_transformation
    df = data_transformation()
    load_pipeline(df, table_name='climate_records')
