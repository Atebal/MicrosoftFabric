# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# 
# # Data science in Microsoft Fabric

# CELL ********************

# Azure storage access info for open dataset diabetes
blob_account_name = "azureopendatastorage"
blob_container_name = "mlsamples"
blob_relative_path = "diabetes"
blob_sas_token = r"" # Blank since container is Anonymous access

# Set Spark config to access  blob storage
wasbs_path = f"wasbs://%s@%s.blob.core.windows.net/%s" % (blob_container_name, blob_account_name, blob_relative_path)
spark.conf.set("fs.azure.sas.%s.%s.blob.core.windows.net" % (blob_container_name, blob_account_name), blob_sas_token)

print("Remote blob path: " + wasbs_path)

df = spark.read.parquet(wasbs_path)

# CELL ********************

display(df)

# CELL ********************

df=df.toPandas()
df.head()

# CELL ********************


# CELL ********************

# Code generated by Data Wrangler for pandas DataFrame

def clean_data(df):
    # Created column 'Risk' from formula
    df['Risk'] = (df['Y']>211.).astype(int)
    return df

df_clean = clean_data(df.copy())
df_clean.head()

# CELL ********************

df_clean.describe()

# CELL ********************

