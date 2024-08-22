# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "36ea0093-42e8-477e-bda7-1fe967c2d5d1",
# META       "default_lakehouse_name": "MyLakeHouse",
# META       "default_lakehouse_workspace_id": "df9b746e-1b1e-4534-972a-a6ccf9f3715a",
# META       "known_lakehouses": [
# META         {
# META           "id": "36ea0093-42e8-477e-bda7-1fe967c2d5d1"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

 # Azure Blob Storage access info
 blob_account_name = "azureopendatastorage"
 blob_container_name = "nyctlc"
 blob_relative_path = "yellow"
    
 # Construct connection path
 wasbs_path = f'wasbs://{blob_container_name}@{blob_account_name}.blob.core.windows.net/{blob_relative_path}'
 print(wasbs_path)
    
 # Read parquet data from Azure Blob Storage path
 blob_df = spark.read.parquet(wasbs_path)

# CELL ********************

file_name="yellow_taxi"

output_parquet_path=f"abfss://MyDp600@onelake.dfs.fabric.microsoft.com/MyLakeHouse.Lakehouse/Files/RawData/{file_name}"
print(output_parquet_path)

blob_df.limit(1000).write.mode("overwrite").parquet(output_parquet_path)

# CELL ********************

from pyspark.sql.functions import col,to_timestamp,current_timestamp,year,month

raw_df=spark.read.parquet(output_parquet_path)

filtered_df=raw_df.withColumn("dataload_datetime",current_timestamp())

filtered_df=filtered_df.filter(raw_df["storeAndFwdFlag"].isNotNull())

table_name="yellow_taxi"

filtered_df.write.format("delta").mode("append").saveAsTable(table_name)
display(filtered_df.limit(1))

# CELL ********************

from pyspark.sql.functions import col, to_timestamp, current_timestamp, year, month
 
 # Read the parquet data from the specified path
raw_df = spark.read.parquet(output_parquet_path)    

 # Add dataload_datetime column with current timestamp
opt_df = raw_df.withColumn("dataload_datetime", current_timestamp())
    
 # Filter columns to exclude any NULL values in storeAndFwdFlag
opt_df = opt_df.filter(opt_df["storeAndFwdFlag"].isNotNull())

spark.conf.set("spark.sql.parquet.vorder.enabled","true")

table_name = "yellow_taxi_opt"  # New table name
opt_df.write.format("delta").mode("append").saveAsTable(table_name)
    
 # Display results
display(opt_df.limit(1))





# CELL ********************

delta_table_name="yellow_taxi"

table_df=spark.read.format("delta").table(delta_table_name)

table_df.createOrReplaceTempView("yellow_taxi_temp")

table_df=spark.sql('SELECT * FROM yellow_taxi_temp')

display(table_df.limit(10))


# CELL ********************

delta_table_name="yellow_taxi_opt"

opttable_df =spark.read.format("delta").table(delta_table_name)

opttable_df.createOrReplaceTempView("yellow_taxi_opt")

opttable_df=spark.sql("select * from yellow_taxi_opt")

display(opttable_df.limit(10))


# CELL ********************

