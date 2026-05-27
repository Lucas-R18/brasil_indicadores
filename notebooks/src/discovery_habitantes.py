# Databricks notebook source
# ==================== IMPORT LIBS ====================
from datetime   import datetime
from pathlib    import Path

import pandas   as pd

import configparser
import requests
import json
import os 

# from pyspark.sql.functions import current_timestamp

# COMMAND ----------

# ==================== READ CONFIG INI ====================
config = configparser.ConfigParser()
config.read(r"/Workspace/Users/lucas.srodrigues1805@gmail.com/brasil_indicadores/ini/config.ini")

# ==================== DEFINE VARIABLES ====================
project_path        = Path(config.get('config','project_path'))
landing_zone_path   = project_path / Path(config.get('etl','landing_zone_path'))

year_start = curent_year = datetime.now().year -2
year_end = curent_year = datetime.now().year -1


# COMMAND ----------

for year in range(year_start, year_end+1):
    
    api_url = f"https://apisidra.ibge.gov.br/values/t/6579/n6/all/v/all/p/{year}"

    response = requests.get(api_url)
    response.raise_for_status()
    data =  response.json()

    file_path = landing_zone_path / f"estimativa_populacao_municipios_{year}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



# COMMAND ----------

new_columns = [
    "municipio_codigo",        # D1C
    "municipio_nome",          # D1N
    "variavel_codigo",         # D2C
    "variavel_nome",           # D2N
    "ano_codigo",              # D3C
    "ano",                     # D3N
    "unidade_medida_codigo",   # MC
    "unidade_medida",          # MN
    "nivel_territorial_codigo",# NC
    "nivel_territorial",       # NN
    "valor"                    # V
]

df = (
    spark.read
         .option("multiline", "true")
         .option("header", "true")
         .json(str(landing_zone_path))
         .toDF(*new_columns) 
)

df = df.where(
    df.municipio_codigo != 'Município (Código)'
)
