import requests
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("=" * 50)
print("INICIANDO SCRIPT")
print("=" * 50)


def extract_weather_data(url:str) -> list:
    print("Dentro da função extract_weather_data")
    
    try:
        print("Fazendo requisição...")
        response = requests.get(url)
        print(f"Status code: {response.status_code}")
        
        if response.status_code != 200:
            logging.error(f"Erro na requisição: {response.status_code}")
            return []
        
        data = response.json()
        print(f"Dados recebidos: {len(str(data))} caracteres")
        
        if not data:
            logging.warning("Nenhum dado encontrado.")
            return []
        
        output_path = Path('data/weather_data.json')
        output_dir = Path(output_path).parent
        print(f"Criando diretório: {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)   
        
        print(f"Salvando em: {output_path}")
        with open(output_path, 'w') as f: 
            json.dump(data, f, indent=4)
        
        logging.info(f"Dados extraídos e salvos em {output_path}")
        return data
    
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
        return []

