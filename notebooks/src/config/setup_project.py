# Databricks notebook source
# ================= IMPORT CONFIG PROJECT =================

# COMMAND ----------

# MAGIC %run ../utils/config_project

# COMMAND ----------

from pathlib import Path
import os

# COMMAND ----------

config          = config_ini()
project_path    = Path(config.get('config','project_path'))

# COMMAND ----------

# ==================== READ FILE CONFIG INI ====================
config = config_ini()

# ==================== DEFINE VARIABLES ====================
project_path   = Path(config.get('config','project_path'))

# COMMAND ----------


# ==================== CREATE FOLDERS ====================
Path(f"{project_path}/data/landing_zone").mkdir(parents=True,exist_ok=True)
Path(f"{project_path}/data/bronze").mkdir(parents=True,exist_ok=True)
Path(f"{project_path}/data/silver").mkdir(parents=True,exist_ok=True)
Path(f"{project_path}/data/gold").mkdir(parents=True,exist_ok=True)

Path(f"{project_path}/env").mkdir(parents=True,exist_ok=True)
Path(f"{project_path}/ini").mkdir(parents=True,exist_ok=True)

Path(f"{project_path}/notebooks/src").mkdir(parents=True,exist_ok=True)
Path(f"{project_path}/notebooks/validation").mkdir(parents=True,exist_ok=True)

Path(f"{project_path}/docs").mkdir(parents=True,exist_ok=True)


# COMMAND ----------

# ==================== CREATE .GITIGNORE ====================

#FOLDER DATA
path_data = Path(f"{project_path}/data")
content = "*"

with open(path_data / ".gitignore", "w") as file:
    file.write(content)

#FOLDER ENV
path_env = Path(f"{project_path}/env")

with open(path_env / ".gitignore", "w") as file:
    file.write(content)


# COMMAND ----------

# MAGIC %sql
# MAGIC /* ------------------------------------------------------------------------------------------------------------------------------------ */
# MAGIC -- create database
# MAGIC
# MAGIC create catalog if not exists indicadores_brasil;
# MAGIC
# MAGIC create schema if not exists indicadores_brasil.bronze;
# MAGIC create schema if not exists indicadores_brasil.silver;
# MAGIC create schema if not exists indicadores_brasil.gold;
# MAGIC
# MAGIC
