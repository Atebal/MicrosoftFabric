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
# META           "id": "d4c37493-e4d7-4aba-9bf1-5d137551f7ab"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!


# CELL ********************

df = spark.sql("SELECT * FROM HighLoadLake.cms_provider_drug_costs_star LIMIT 1000")
display(df)

# CELL ********************


# CELL ********************




# Load data into pandas DataFrame from "/lakehouse/default/" + "Files/MUP/MUP_DPR_RY21_P04_V10_DY13_NPIBN_4.csv"
df = spark.read.format("csv").option("header","true").load("Files/MUP/MUP_DPR_RY21_P04_V10_DY13_NPIBN_4.csv")
display(df)


# CELL ********************

