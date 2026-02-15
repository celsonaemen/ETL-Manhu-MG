from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from pathlib import Path
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, '/opt/airflow/src')

from extract_data import extract_weather_data
from transform_data import data_transformation
from load_data import load_pipeline
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)
logger.info(f"📁 .env carregado de: {env_path}")

API_KEY = os.getenv('API_KEY')
URL = f'https://api.openweathermap.org/data/2.5/weather?q=Manhuaçu,BR&appid={API_KEY}&units=metric&lang=pt_br'

DATA_DIR = '/opt/airflow/data'
os.makedirs(DATA_DIR, exist_ok=True)

with DAG(
    dag_id='weather_dag',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5),
    },
    description='Pipeline ETL para dados de clima - Manhuaçu/MG',
    schedule='0 * * * *',
    start_date=datetime(2026, 2, 15),
    catchup=False,
    tags=['weather', 'ETL', 'manhuacu'],
) as dag:

    @task()
    def extract():
        """Extrai dados da API OpenWeather"""
        logger.info("="*50)
        logger.info("🌎 Iniciando extração de MANHUAÇU - MINAS GERAIS")
        extract_weather_data(URL)
        logger.info("✅ Extração concluída")
        return "Extração OK"

    @task()
    def transform():
        """Transforma os dados extraídos"""
        logger.info("="*50)
        logger.info("🔄 Iniciando transformação")
        df = data_transformation()
        logger.info(f"📊 DataFrame: {len(df)} linhas")
        output_path = f'{DATA_DIR}/weather_data.parquet'
        df.to_parquet(output_path, index=False)
        logger.info(f"💾 Arquivo salvo: {output_path}")
        return output_path

    @task()
    def load(file_path: str = f'{DATA_DIR}/weather_data.parquet'):
        """Carrega os dados no banco"""
        logger.info("="*50)
        logger.info(f"📦 Iniciando carga: {file_path}")
        import pandas as pd
        df = pd.read_parquet(file_path)
        logger.info(f"📈 Registros: {len(df)}")
        result = load_pipeline(df, table_name='climate_records')
        logger.info("✅ Carga concluída")
        return "Carga OK"

    extract() >> transform() >> load()
