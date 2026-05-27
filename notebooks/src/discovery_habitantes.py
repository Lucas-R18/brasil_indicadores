# Databricks notebook source
# ==================== IMPORT LIBS ====================
from datetime   import datetime
from pathlib    import Path

import pandas   as pd

import configparser
import requests
import json
import os 

# COMMAND ----------

# ==================== READ CONFIG INI ====================
config = configparser.ConfigParser()
config.read(r"/Workspace/Users/lucas.srodrigues1805@gmail.com/brasil_indicadores/ini/config.ini")

# ==================== DEFINE VARIABLES ====================
project_path        = Path(config.get('config','project_path'))
landing_zone_path   = project_path / Path(config.get('etl','landing_zone_path'))
path_bronze         = project_path / Path(config.get('etl','bronze_path'))

path_estimativa_populacao_municipios = landing_zone_path / f"estimativa_populacao_municipios/"
path_estimativa_populacao_municipios.mkdir(parents=True,exist_ok=True)

# year_start  = 2019
year_start = curent_year = datetime.now().year -2
year_end    = curent_year = datetime.now().year -1


# COMMAND ----------

#request data from sidra ibge
for year in range(year_start, year_end+1):
    
    api_url = f"https://apisidra.ibge.gov.br/values/t/6579/n6/all/v/all/p/{year}"

    response = requests.get(api_url)
    response.raise_for_status()
    data =  response.json()

    path_file = path_estimativa_populacao_municipios / f"{year}.json"

    with open(path_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



# COMMAND ----------

#define collumns to be used
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

#read json files
df = (
    spark.read
         .option("multiline", "true")
         .option("header", "true")
         .json(str(path_estimativa_populacao_municipios))
         .toDF(*new_columns) 
)


# COMMAND ----------

#/* ------------------------------------------------------------------------------------------------------------------------------------ */
#-- create bronze table

(
    df.write
      .format("delta")
      .mode("overwrite")
      .option("overwriteSchema", "true")
      .saveAsTable("indicadores_brasil.bronze.estimativa_populacao_municipios")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC /* ------------------------------------------------------------------------------------------------------------------------------------ */
# MAGIC -- create silver table
# MAGIC
# MAGIC truncate table  indicadores_brasil.silver.estimativa_populacao_municipios;
# MAGIC insert into     indicadores_brasil.silver.estimativa_populacao_municipios  
# MAGIC select
# MAGIC     municipio_codigo
# MAGIC     , trim(split(municipio_nome, ' - ')[0]) AS municipio_nome
# MAGIC     , trim(split(municipio_nome, ' - ')[1]) AS uf_nome
# MAGIC     , variavel_codigo
# MAGIC     , variavel_nome
# MAGIC     , ano_codigo
# MAGIC     , ano
# MAGIC     , unidade_medida_codigo
# MAGIC     , unidade_medida
# MAGIC     , nivel_territorial_codigo
# MAGIC     , nivel_territorial
# MAGIC     , cast(replace(valor,'...',0) as int) as  valor
# MAGIC from 
# MAGIC     indicadores_brasil.bronze.estimativa_populacao_municipios
# MAGIC where
# MAGIC     lower(municipio_codigo) <> lower('Município (Código)');  
