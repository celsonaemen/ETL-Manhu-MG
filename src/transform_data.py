import pandas as pd
from pathlib import Path
import json

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).parent.parent / 'data/weather_data.json'
columns_names_to_drop = ['weather', 'weather_icon', 'sys.type']

columns_to_rename = {
    "base": "base",
    "visibility": "visibility",
    "dt": "dt",
    "timezone": "timezone",
    "id": "city_id",
    "name": "city_name",
    "cod": "code",
    "coord.lon": "longitude",
    "coord.lat": "latitude",
    "main.temp": "temperature",
    "main.feels_like": "feels_like",
    "main.temp_min": "temp_min",
    "main.temp_max": "temp_max",
    "main.pressure": "pressure",
    "main.humidity": "humidity",
    "main.sea_level": "sea_level",
    "main.grnd_level": "grnd_level",
    "wind.speed": "wind_speed",
    "wind.deg": "wind_deg",
    "wind.gust": "wind_gust",
    "clouds.all": "clouds",
    "sys.id": "sys_id",
    "sys.country": "country",
    "sys.sunrise": "sunrise",
    "sys.sunset": "sunset"
}

columns_to_normalize = ['dt', 'sunrise', 'sunset']


def create_dataframe(path_name: str) -> pd.DataFrame:
    logging.info("->Carregando dados do arquivo json")
    path = path_name

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with open(path) as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    logging.info(f"->Dataframe criado com {len(df)} linhas e {len(df.columns)} colunas")
    return df


def normalize_weather_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("->Normalizando coluna 'weather'")
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))

    df_weather = df_weather.rename(columns={
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })

    df = pd.concat([df, df_weather], axis=1)
    logging.info(f"->Dataframe normalizado com {len(df)} linhas e {len(df.columns)} colunas")
    return df


def drop_columns(df: pd.DataFrame, colums_names: list[str]) -> pd.DataFrame:
    logging.info(f"->Removendo colunas: {colums_names}")
    df = df.drop(columns=colums_names, errors='ignore')
    logging.info(f"->Colunas removidas - {len(df.columns)} colunas restantes")
    return df


def rename_columns(df: pd.DataFrame, columns_names: dict[str, str]) -> pd.DataFrame:
    logging.info(f"->Renomeando {len(columns_names)} colunas...")
    df = df.rename(columns=columns_names)
    logging.info("->Colunas renomeadas")
    return df


def normalize_datetime_columns(df: pd.DataFrame, columns_names: list[str]) -> pd.DataFrame:
    logging.info(f"->Normalizando colunas de data/hora: {columns_names}")
    for name in columns_names:
        if name in df.columns:
            df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')
            logging.info(f"->Coluna '{name}' normalizada")
    return df


def data_transformation():
    print("\n" + "="*50)
    print("Iniciando transformações de dados...")
    print("="*50 + "\n")
    
    df = create_dataframe(path_name)
    df = normalize_weather_dataframe(df)
    df = drop_columns(df, columns_names_to_drop)
    df = rename_columns(df, columns_to_rename)
    df = normalize_datetime_columns(df, columns_to_normalize)
    
    logging.info("\n->Transformações de dados concluídas")
    logging.info(f"->DataFrame final: {len(df)} linhas e {len(df.columns)} colunas\n")
    
    return df


if __name__ == "__main__":
    df_transformed = data_transformation()
    print("\nPrimeiras linhas do DataFrame transformado:")
    print(df_transformed.head())
    print("\nInformações do DataFrame:")
    print(df_transformed.info())