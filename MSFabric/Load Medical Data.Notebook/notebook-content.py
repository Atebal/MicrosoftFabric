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


# CELL ********************

spark.sql("DROP Table if EXISTS cms_provider_drug_costs")

# CELL ********************

file_dict={
    2013 : "Files/MUP/MUP_DPR_RY21_P04_V10_DY13_NPIBN_4.csv",                 
                2014 : "Files/MUP/MUP_DPR_RY21_P04_V10_DY14_NPIBN_1.csv",
                2015 :  "Files/MUP/MUP_DPR_RY21_P04_V10_DY15_NPIBN_1.csv",
                2016 : "Files/MUP/MUP_DPR_RY21_P04_V10_DY16_NPIBN_0.csv",
                2017 : "Files/MUP/MUP_DPR_RY21_P04|_V10_DY17_NPIBN_1.csv",
                2018 : "Files/MUP/MUP_DPR_RY21_P04_V10_DY18_NPIBN_0.csv",
                2019 : "Files/MUP/MUP_DPR_RY21_P04_V10_DY19_NPIBN_1.csv",
                2020 : "Files/MUP/MUP_DPR_RY22_P04_V10_DY20_NPIBN_0.csv",
                2021 : "Files/MUP/MUP_DPR_RY23_P04_V10_DY21_NPIBN.csv"
}

# CELL ********************

from pyspark.sql.types import LongType,DecimalType
from pyspark.sql.functions import lit,col,concat

for key,v in file_dict.items():
    print(f"key: {key}, value: {v}")

    df=spark.read.format("csv").option("header","true").option("inferschema","true").load(v)
    df=df.withColumn("Year",lit(key)) \
       .withColumn("Tot_Drug_Cst",df.Tot_Drug_Cst.cast(DecimalType(10,2))) \
       .withColumn("Tot_30day_Fills", df.Tot_30day_Fills.cast(DecimalType(10,2))) \
       .withColumn("GE65_Tot_30day_Fills",df.GE65_Tot_30day_Fills.cast(DecimalType(10,2))) \
       .withColumn("GE65_Tot_Drug_Cst",df.GE65_Tot_Drug_Cst.cast(DecimalType(10,2))) \
       .withColumn("Prscrbr_City_State",concat(df.Prscrbr_City,lit(" "),df.Prscrbr_State_Abrvtn))\
       .withColumn("Prscrbr_Full_Name",concat(df.Prscrbr_Last_Org_Name,lit(" "),df.Prscrbr_First_Name)) \
       .withColumn("Tot_Clms",df.Tot_Clms.cast(LongType())) \
       .withColumn("Tot_Day_Suply",df.Tot_Day_Suply.cast(LongType())) \
       .withColumn("Tot_Benes",df.Tot_Benes.cast(LongType())) \
       .withColumn("GE65_Tot_Clms",df.GE65_Tot_Clms.cast(LongType())) \
       .withColumn("GE65_Tot_Benes",df.GE65_Tot_Benes.cast(LongType())) \
       .withColumn("GE65_Tot_Day_Suply",df.GE65_Tot_Day_Suply.cast(LongType())) 

  #  display(df)
    print(f"writing data to table-{df.count()} records")

    
    df.write.mode("append").format('delta').save(f"Tables/cms_provider_drug_costs")


# CELL ********************

df=spark.read.table("cms_provider_drug_costs")
display(df)

# CELL ********************

print(df.count())

# CELL ********************

df.printSchema()

# CELL ********************

# MAGIC %%sql
# MAGIC select sum(Tot_Day_Suply) from cms_provider_drug_costs

# METADATA ********************

# META {
# META   "language": "sparksql"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC DESCRIBE DETAIL cms_provider_drug_costs

# METADATA ********************

# META {
# META   "language": "sparksql"
# META }

# CELL ********************

