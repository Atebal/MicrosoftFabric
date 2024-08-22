# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "d4c37493-e4d7-4aba-9bf1-5d137551f7ab",
# META       "default_lakehouse_name": "HighLoadLake",
# META       "default_lakehouse_workspace_id": "df9b746e-1b1e-4534-972a-a6ccf9f3715a",
# META       "known_lakehouses": [
# META         {
# META           "id": "36ea0093-42e8-477e-bda7-1fe967c2d5d1"
# META         },
# META         {
# META           "id": "d4c37493-e4d7-4aba-9bf1-5d137551f7ab"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.conf.set("spark.sql.parquet.vorder.enable","true")
spark.conf.set("spark.microsoft.delta.optimizeWrite.enabled","true")
spark.conf.set("spark.microsoft.delta.optimizeWrite.binSize","1073741824")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col,year,month,quarter

table_name='fact_sale'

df=spark.read.format("parquet").load('Files/wwi-raw-data/full/fact_sale_1y_full')
df=df.withColumn('Year',year(col('InvoiceDateKey')))
df=df.withColumn('Quarter',quarter(col('InvoiceDateKey')))
df=df.withColumn('Month',month(col('InvoiceDateKey')))

df.write.format("delta").partitionBy('Year','Quarter').save("Tables/" + table_name)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.types import *

def loadFullDataFromSource(table_name):
    df=spark.read.format("parquet").load('Files/wwi-raw-data/full/' + table_name)
    df=df.drop("Photo")
    df.write.mode("overwrite").format("delta").save("Tables/" + table_name)

full_tables=[
    'dimension_city',
    'dimension_date',
    'dimension_employee',
    'dimension_stock_item'
]

for table in full_tables:
    loadFullDataFromSource(table)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
