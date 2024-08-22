# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "d4c37493-e4d7-4aba-9bf1-5d137551f7ab",
# META       "default_lakehouse_name": "",
# META       "default_lakehouse_workspace_id": "",
# META       "known_lakehouses": [
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
from powerbiclient import QuickVisualize,get_dataset_config,Report

df=spark.read.format('csv').load("Files/orders/*.csv")
pbi_visulaize=QuickVisualize(get_dataset_config(df))
pbi_visulaize

# CELL ********************

df.write.format('delta').saveAsTable("orders",path="Files/table")

# CELL ********************

