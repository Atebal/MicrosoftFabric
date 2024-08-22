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


dim_year_df=spark.sql("SELECT DISTINCT Year,CONCAT(CAST(Year AS string),'-01-01') AS Year_Date_Key from cms_provider_drug_costs" )

display(dim_year_df)

# CELL ********************

from pyspark.sql.types import DateType
from pyspark.sql.functions import col

dim_year_df=dim_year_df.withColumn("Year_Date_Key",col("Year_Date_Key").cast(DateType()))

display(dim_year_df)

# CELL ********************

dim_year_df.printSchema()

# CELL ********************

dim_year_df.write.mode("overwrite").format("delta").save("Tables/cms_provider_dim_year")

# CELL ********************

dim_geo_df = spark.sql('''SELECT Prscrbr_City, Prscrbr_City_State, Prscrbr_State_Abrvtn, Prscrbr_State_FIPS, MAX(Year) AS Max_Year, MIN(Year) AS Min_Year,
    row_number() OVER (ORDER BY Prscrbr_State_Abrvtn,Prscrbr_City_State ASC) AS geo_key
    FROM cms_provider_drug_costs
    GROUP BY Prscrbr_City,Prscrbr_City_State,Prscrbr_State_Abrvtn,Prscrbr_State_FIPS ''')

#print(dim_geo_df.count())
display(dim_geo_df)

# CELL ********************

dim_geo_df.write.mode("overwrite").format("delta").save("Tables/cms_provider_dim_geography")

# CELL ********************

dim_provider_df = spark.sql('''SELECT Prscrbr_First_Name
,Prscrbr_Full_Name
,Prscrbr_Last_Org_Name
,Prscrbr_NPI
,Prscrbr_Type
,Prscrbr_Type_Src
,MAX(Year) AS Max_Year
,MIN(Year) AS Min_Year
,row_number() OVER (ORDER BY Prscrbr_Full_Name,Prscrbr_NPI,Prscrbr_Type,Prscrbr_Type_Src ASC) AS provider_key
FROM cms_provider_drug_costs
GROUP BY Prscrbr_First_Name,Prscrbr_Full_Name,Prscrbr_Last_Org_Name,Prscrbr_NPI,Prscrbr_Type,Prscrbr_Type_Src''')


# CELL ********************

dim_provider_df.write.mode("overwrite").format("delta").save("Tables/cms_provider_dim_provider")

# CELL ********************

dim_drug_df = spark.sql('''SELECT Brnd_Name
,Gnrc_Name
,MAX(Year) AS Max_Year
,MIN(Year) AS Min_Year
,row_number() OVER (ORDER BY Brnd_Name,Gnrc_Name ASC) AS drug_key
FROM cms_provider_drug_costs
GROUP BY Brnd_Name, Gnrc_Name''')

# CELL ********************

dim_drug_df.write.mode("overwrite").format("delta").save("Tables/cms_provider_dim_drug")

# CELL ********************

drug_costs_star_df = spark.sql('''SELECT GE65_Bene_Sprsn_Flag
,GE65_Sprsn_Flag
,GE65_Tot_30day_Fills
,GE65_Tot_Benes
,GE65_Tot_Clms
,GE65_Tot_Day_Suply
,GE65_Tot_Drug_Cst
,Tot_30day_Fills
,Tot_Benes
,Tot_Clms
,Tot_Day_Suply
,Tot_Drug_Cst
,Year
,b.drug_key
,c.geo_key
,d.provider_key
FROM cms_provider_drug_costs a
LEFT OUTER JOIN cms_provider_dim_drug b ON a.Brnd_Name = b.Brnd_Name AND a.Gnrc_Name = b.Gnrc_Name
LEFT OUTER JOIN cms_provider_dim_geography c ON a.Prscrbr_City_State IS NOT DISTINCT FROM c.Prscrbr_City_State 
LEFT OUTER JOIN cms_provider_dim_provider d ON a.Prscrbr_Full_Name IS NOT DISTINCT FROM d.Prscrbr_Full_Name AND a.Prscrbr_NPI = d.Prscrbr_NPI AND a.Prscrbr_Type IS NOT DISTINCT FROM d.Prscrbr_Type AND a.Prscrbr_Type_Src = d.Prscrbr_Type_Src''')


# CELL ********************

drug_costs_star_df.write.mode("overwrite").format("delta").save("Tables/cms_provider_drug_costs_star")

# CELL ********************

