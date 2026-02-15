# 🌤️ PROJETO WEATHER ETL - DOCUMENTAÇÃO COMPLETA

**Data:** 14-15 de Fevereiro de 2026  
**Desenvolvedor:** Gutocodes_
---

## 📋 RESUMO EXECUTIVO

Projeto completo de **Pipeline ETL (Extract, Transform, Load)** para coleta automatizada de dados climáticos usando:
- Python + Pandas
- PostgreSQL
- Docker + Docker Compose
- Apache Airflow
- API OpenWeather

**Status:** ✅ **FUNCIONANDO 100%**

---

## 🛠️ STACK TECNOLÓGICA

### Ambiente de Desenvolvimento
- **SO:** Windows 11 + WSL2 (Ubuntu 24.04)
- **IDE:** VS Code
- **Terminal:** WSL Ubuntu
- **Containerização:** Docker Desktop

### Backend
- **Linguagem:** Python 3.12.3
- **Gerenciador de Pacotes:** uv
- **Banco de Dados:** PostgreSQL 16
- **Orquestrador:** Apache Airflow 2.10.4

### Bibliotecas Python
```txt
pandas==3.0.0
numpy==2.4.2
sqlalchemy==2.0.46
psycopg2-binary==2.9.11
requests==2.32.5
python-dotenv==1.2.1
ipykernel==7.2.0
jupyter==1.1.1
jupyterlab==4.5.4
notebook==7.5.3
```

---

## 📁 ESTRUTURA DO PROJETO

```
VS CODE PROJECTS/
├── config/
│   └── .env                    # Variáveis de ambiente
├── dags/
│   └── weather_etl_dag.py      # DAG do Airflow
├── data/
│   └── weather_data.json       # Dados brutos da API
├── notebooks/
│   └── analysis_data.ipynb     # Análise exploratória
├── src/
│   ├── extract_data.py         # Extração da API
│   ├── transform_data.py       # Transformação com Pandas
│   └── load_data.py            # Carga no PostgreSQL
├── docker-compose.yml          # Orquestração Docker
├── .gitignore                  # Arquivos ignorados pelo Git
├── main.py                     # Pipeline ETL completo
├── pyproject.toml              # Configuração do projeto
└── README.md                   # Documentação
```

---

## 🚀 INSTALAÇÃO E CONFIGURAÇÃO

### 1. WSL + Ubuntu
```bash
wsl --version
```

### 2. Python e Ferramentas
```bash
# Python
sudo apt install python-is-python3

# PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib postgresql-client -y
sudo service postgresql start

# Git
git --version  # v2.43.0 
git config --global user.name "Gutocodes"
git config --global user.email "juniordalla7@gmail.com"
```

### 3. UV (Gerenciador de Pacotes)
```bash
# UV 
uv --version  # 0.10.0
```

### 4. Projeto Python
```bash
cd "/mnt/c/Users/gutoc/Desktop/VS CODE PROJECTS"

# Criar ambiente virtual
uv venv

# Ativar ambiente
source .venv/bin/activate

# Instalar dependências
uv add pandas
uv add sqlalchemy
uv add psycopg2-binary
uv add requests
uv add python-dotenv
uv add jupyter jupyterlab notebook ipykernel
```

### 5. Docker Desktop
- Baixar e instalar Docker Desktop para Windows
- Ativar integração com WSL2:
  - Settings → Resources → WSL Integration
  - ✅ Enable integration with my default WSL distro
  - ✅ Ubuntu
  - Apply & Restart

### 6. PostgreSQL
```bash
# Criar usuário e banco
sudo -u postgres psql

-- No PostgreSQL:
CREATE USER angeldarkblue WITH PASSWORD '123';
ALTER USER angeldarkblue WITH SUPERUSER;
CREATE DATABASE weather_warehouse OWNER angeldarkblue;

-- Criar tabela
\c weather_warehouse

CREATE TABLE climate_records (
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
    country VARCHAR(10),
    sunrise TIMESTAMP WITH TIME ZONE,
    sunset TIMESTAMP WITH TIME ZONE,
    weather_id INTEGER,
    weather_main VARCHAR(50),
    weather_description VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🐳 DOCKER + AIRFLOW

### docker-compose.yml
```yaml
version: '3.8'

services:
  # Banco de dados do projeto
  postgres:
    image: postgres:16
    container_name: weather-postgres
    environment:
      POSTGRES_USER: angeldarkblue
      POSTGRES_PASSWORD: 123
      POSTGRES_DB: weather_warehouse
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # Banco do Airflow
  airflow-db:
    image: postgres:16
    container_name: airflow-postgres
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - airflow_db_data:/var/lib/postgresql/data

  # Airflow Standalone
  airflow:
    image: apache/airflow:2.10.4-python3.12
    container_name: airflow-standalone
    depends_on:
      - postgres
      - airflow-db
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@airflow-db/airflow
      _AIRFLOW_WWW_USER_USERNAME: admin
      _AIRFLOW_WWW_USER_PASSWORD: admin
      _PIP_ADDITIONAL_REQUIREMENTS: 'pandas sqlalchemy psycopg2-binary requests python-dotenv'
    volumes:
      - ./dags:/opt/airflow/dags
      - ./src:/opt/airflow/src
      - ./config:/opt/airflow/config
      - ./data:/opt/airflow/data
    ports:
      - "8080:8080"
    command: standalone

volumes:
  postgres_data:
  airflow_db_data:
  airflow_logs:
```

### Comandos Docker
```bash
# Subir containers
docker compose up -d

# Ver status
docker compose ps

# Ver logs
docker compose logs -f airflow

# Parar tudo
docker compose down

# Parar e remover volumes
docker compose down -v

# Reiniciar serviço específico
docker compose restart airflow
```

---

## 🔑 CREDENCIAIS E CONFIGURAÇÕES

### PostgreSQL (Local - WSL)
- **Host:** localhost
- **Porta:** 5432
- **Usuário:** angeldarkblue
- **Senha:** 
- **Database:** weather_warehouse

### PostgreSQL (Docker)
- **Host:** localhost (ou nome do container)
- **Porta:** 5432
- **Usuário:** angeldarkblue
- **Senha:** 
- **Database:** weather_warehouse

### Airflow
- **URL:** http://localhost:8080
- **Usuário:** admin
- **Senha:** 
  - *Nota: A senha muda a cada vez que recria os containers*

### API OpenWeather
- **API Key:** 
- **Cidade:** Manhuaçu, BR
- **URL:** `https://api.openweathermap.org/data/2.5/weather?q=Manhuacu,BR&units=metric&appid={API_KEY}`

### Arquivo .env
```env
# config/.env
DB_USER=angeldarkblue
DB_PASSWORD=123
DB_NAME=weather_warehouse
DB_HOST=localhost
DB_PORT=5432

API_KEY=
CITY=Manhuacu
```

---

## 📊 PIPELINE ETL

### 1. Extract (src/extract_data.py)
- Busca dados da API OpenWeather
- Cidade: Manhuaçu, MG, Brasil
- Salva JSON em `data/weather_data.json`
- Última coleta: 19.19°C, Céu limpo, 93% umidade

### 2. Transform (src/transform_data.py)
- Carrega JSON
- Normaliza coluna 'weather' (nested JSON)
- Remove colunas desnecessárias
- Renomeia colunas para inglês
- Converte timestamps para timezone America/Sao_Paulo
- Output: DataFrame com 27 colunas

### 3. Load (src/load_data.py)
- Conecta no PostgreSQL
- Cria tabela se não existir
- Insere dados usando pandas.to_sql()
- Verifica registros inseridos

### Executar Pipeline Completo
```bash
# Ativar ambiente
source .venv/bin/activate

# Rodar pipeline
uv run main.py
```

---

## 🔄 AIRFLOW DAG

### Agendamento
- **Frequência:** A cada 6 horas
- **Cron:** `0 */6 * * *`
- **Início:** 15/02/2026

### Tasks
1. **extract_weather_data** → Busca dados da API
2. **transform_data** → Limpa e organiza dados
3. **load_to_database** → Salva no PostgreSQL

### Arquivo: dags/weather_etl_dag.py
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Importa funções do projeto
from src.extract_data import extract_weather_data
from src.transform_data import data_transformation
from src.load_data import load_pipeline

# Configurações
default_args = {
    'owner': 'gutocodes',
    'start_date': datetime(2026, 2, 15),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG
dag = DAG(
    'weather_etl_pipeline',
    default_args=default_args,
    schedule_interval='0 */6 * * *',
    catchup=False,
)

# Tasks
extract = PythonOperator(task_id='extract', python_callable=extract_weather_data, dag=dag)
transform = PythonOperator(task_id='transform', python_callable=data_transformation, dag=dag)
load = PythonOperator(task_id='load', python_callable=load_pipeline, dag=dag)

# Ordem
extract >> transform >> load
```

---

## 🐛 PROBLEMAS RESOLVIDOS

### 1. WSL não reconhecia comandos
**Problema:** `python`, `psql`, `docker-compose` não encontrados  
**Solução:** Usar caminhos Linux `/mnt/c/...` e instalar ferramentas no WSL

### 2. PostgreSQL não conectava do WSL
**Problema:** PostgreSQL do Windows não aceita conexões do WSL  
**Solução:** Instalar PostgreSQL direto no WSL ou usar Docker

### 3. Docker compose não funcionava
**Problema:** Docker Desktop não integrado com WSL  
**Solução:** Settings → Resources → WSL Integration → Ativar Ubuntu

### 4. Airflow não aceitava login
**Problema:** Senha gerada automaticamente, não era "admin"  
**Solução:** Ver senha nos logs: `docker compose logs airflow | grep password`

### 5. Tabela PostgreSQL sem colunas
**Problema:** DataFrame tinha mais colunas que a tabela  
**Solução:** Recriar tabela com TODAS as 27 colunas

### 6. Jupyter Kernel não aparecia
**Problema:** VS Code não detectava kernel do .venv  
**Solução:** 
- Ativar extensão WSL no VS Code
- Abrir projeto remotamente no WSL
- Instalar ipykernel no ambiente virtual

---

## 📈 DADOS COLETADOS

### Exemplo de Registro
```json
{
  "cidade": "Manhuaçu",
  "temperatura": 19.19,
  "sensacao_termica": 19.59,
  "umidade": 93,
  "pressao": 1018,
  "vento": 0.67,
  "clima": "Clear - clear sky",
  "timestamp": "2026-02-14 21:50:57-03:00"
}
```

### Estatísticas
- **Total de registros:** 1 (primeira execução bem-sucedida)
- **Cidade monitorada:** Manhuaçu, MG, Brasil
- **Coordenadas:** -20.2581, -42.0336
- **Fuso horário:** America/Sao_Paulo (UTC-3)

---

## 🎯 COMANDOS ÚTEIS

### Ambiente Python
```bash
# Ativar ambiente
source .venv/bin/activate

# Listar pacotes
uv pip list

# Adicionar pacote
uv add nome-pacote
```

### PostgreSQL
```bash
# Conectar (WSL)
sudo -u postgres psql -d weather_warehouse

# Conectar (Docker)
docker exec -it weather-postgres psql -U angeldarkblue -d weather_warehouse

# Consultas úteis
SELECT * FROM climate_records ORDER BY dt DESC LIMIT 10;
SELECT COUNT(*) FROM climate_records;
SELECT city_name, AVG(temperature) FROM climate_records GROUP BY city_name;
```

### Docker
```bash
# Status
docker compose ps

# Logs
docker compose logs -f [service]

# Reiniciar
docker compose restart [service]

# Parar e remover
docker compose down -v

# Entrar no container
docker exec -it airflow-standalone bash
```

### Git
```bash
# Inicializar
git init

# Status
git status

# Adicionar arquivos
git add .

# Commit
git commit -m "mensagem"

# Ver histórico
git log --oneline
```

---

## 📚 PRÓXIMOS PASSOS

### Melhorias Sugeridas



   **Múltiplas Cidades**
   - [ ] Criar loop para coletar dados de várias cidades
   - [ ] Adicionar lista de cidades no .env

   **Análise de Dados**
   - [ ] Criar notebook com análises estatísticas
   - [ ] Gráficos de temperatura ao longo do tempo
   - [ ] Comparação entre cidades

   **Dashboard**
   - [ ] Streamlit ou Dash para visualização
   - [ ] Gráficos interativos
   - [ ] Alertas de temperatura

   **Notificações**
   - [ ] Email quando temperatura passar de X graus
   - [ ] Slack/Discord notifications

   **Testes**
   - [ ] Testes unitários com pytest
   - [ ] CI/CD com GitHub Actions

    **Documentação**
   - [ ] README.md detalhado
   - [ ] Docstrings em todas as funções
   - [ ] Swagger/OpenAPI se criar API

---

## 🎓 APRENDIZADOS

### Conceitos Técnicos Dominados
✅ Pipeline ETL (Extract, Transform, Load)  
✅ Python para Data Engineering  
✅ Pandas para manipulação de dados  
✅ SQLAlchemy ORM  
✅ PostgreSQL (instalação, configuração, queries)  
✅ Docker + Docker Compose  
✅ Apache Airflow (DAGs, scheduling)  
✅ WSL2 (integração Windows + Linux)  
✅ Git (básico)  
✅ APIs REST  
✅ Environment variables (.env)  
✅ Jupyter Notebooks  

### Soft Skills
✅ Debugging e resolução de problemas  
✅ Leitura de logs e mensagens de erro  
✅ Pesquisa e adaptação de soluções  
✅ Persistência (muitos erros resolvidos!)  
✅ Documentação de código  

---

## 🙏 AGRADECIMENTOS
 
**OpenWeather API:** Dados climáticos gratuitos  
**Apache Airflow:** Ferramenta open-source incrível  
**Comunidade Python:** Bibliotecas e documentação excelentes  

---

## 📝 NOTAS FINAIS


**Data de conclusão:** 15/02/2026  
**Tempo total:** ~8 horas (distribuídas em 2 dias)  
**Status:** ✅ PROJETO FUNCIONAL E DEPLOYADO  

---

## 📧 CONTATO

**Desenvolvedor:** Gutocodes  
**Email:** GUTOCODES@OUTLOOK.COM  
**GitHub:** CELSONAMEN 
**Localização:** Manhuaçu, MG, Brasil  
