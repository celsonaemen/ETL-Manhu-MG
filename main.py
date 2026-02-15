# from src.extract_data import extract_weather_data
# from src.load_data import load_pipeline
# from src.transform_data import data_transformation
# import os 
# from pathlib import Path
# from dotenv import load_dotenv
# import logging

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# env_path = Path(__file__).resolve().parent / 'config/.env'
# load_dotenv(env_path)

# API_KEY = os.getenv('API_KEY', 'a6a6903d7e9f5cb13096e26339b27bae')
# CITY = os.getenv('CITY', 'Manhuacu')
# url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY},BR&appid={API_KEY}&units=metric'

# table_name = 'climate_records'


# def pipeline():
#     """Pipeline ETL completo: Extract -> Transform -> Load"""
#     print("\n" + "=" * 60)
#     print("INICIANDO PIPELINE ETL - DADOS CLIMÁTICOS")
#     print("=" * 60 + "\n")
    
#     try:
#         # EXTRACT
#         logging.info("ETAPA 1: Extração de dados da API")
#         extract_weather_data(url)
        
#         # TRANSFORM
#         logging.info("\nETAPA 2: Transformação de dados")
#         df = data_transformation()
        
#         # LOAD
#         logging.info("\nETAPA 3: Carga de dados no banco")
#         load_pipeline(df, table_name=table_name)
        
#         print("\n" + "=" * 60)
#         print("✅ PIPELINE EXECUTADA COM SUCESSO!")
#         print("=" * 60 + "\n")
        
#     except Exception as e:
#         logging.error(f"❌ Erro na execução da pipeline: {e}")
#         import traceback
#         traceback.print_exc()


# if __name__ == "__main__":
#     pipeline()