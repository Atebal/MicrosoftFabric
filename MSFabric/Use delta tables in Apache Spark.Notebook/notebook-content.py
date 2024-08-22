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

df = spark.read.format("csv").option("header","true").load("Files/products/products.csv")
# df now is a Spark DataFrame containing CSV data from "Files/products/products.csv".
display(df)

# CELL ********************

df.write.format("delta").saveAsTable("managed_products")

# CELL ********************

df.write.format("delta").saveAsTable("external_products", path="abfss://1bb8e816-a170-468a-959f-db273b471f1b@onelake.dfs.fabric.microsoft.com/f22dcaa6-2768-4b0c-9cff-19d473724a14/Files/external_products")

# CELL ********************

# MAGIC %%sql
# MAGIC DESCRIBE FORMATTED managed_products;

# METADATA ********************

# META {
# META   "language": "sparksql"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC DESCRIBE FORMATTED external_products

# METADATA ********************

# META {
# META   "language": "sparksql"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC DROP TABLE managed_products;
# MAGIC DROP TABLE external_products;

# METADATA ********************

# META {
# META   "language": "sparksql"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC create table products
# MAGIC using DELTA
# MAGIC location 'Files/external_products';

# METADATA ********************

# META {
# META   "language": "sparksql"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC select * from products;

# METADATA ********************

# META {
# META   "language": "sparksql"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC UPDATE products 
# MAGIC set ListPrice =ListPrice *0.9
# MAGIC where category='ListPrice ';

# METADATA ********************

# META {
# META   "language": "sparksql"
# META }

# CELL ********************

# MAGIC %%sql 
# MAGIC DESCRIBE HISTORY products;

# METADATA ********************

# META {
# META   "language": "sparksql"
# META }

# CELL ********************

delta_table_path='Files/external_products'
current_data=spark.read.format("delta").load(delta_table_path)
display(current_data)

original_data=spark.read.format("delta").option("VersionAsOf",0).load(delta_table_path)
display(original_data)

# CELL ********************

from notebookutils import mssparkutils
from pyspark.sql.types import *
from pyspark.sql.functions import *

# Create a folder
inputPath = 'Files/data/'
mssparkutils.fs.mkdirs(inputPath)

# Create a stream that reads data from the folder, using a JSON schema
jsonSchema = StructType([
StructField("device", StringType(), False),
StructField("status", StringType(), False)
])
iotstream = spark.readStream.schema(jsonSchema).option("maxFilesPerTrigger", 1).json(inputPath)

# Write some event data to the folder
device_data = '''{"device":"Dev1","status":"ok"}
{"device":"Dev1","status":"ok"}
{"device":"Dev1","status":"ok"}
{"device":"Dev2","status":"error"}
{"device":"Dev1","status":"ok"}
{"device":"Dev1","status":"error"}
{"device":"Dev2","status":"ok"}
{"device":"Dev2","status":"error"}
{"device":"Dev1","status":"ok"}'''
mssparkutils.fs.put(inputPath + "data.txt", device_data, True)
print("Source stream created...")

# CELL ********************

# Write the stream to a delta table
delta_stream_table_path = 'Tables/iotdevicedata'
checkpointpath = 'Files/delta/checkpoint'
deltastream = iotstream.writeStream.format("delta").option("checkpointLocation", checkpointpath).start(delta_stream_table_path)
print("Streaming to delta sink...")

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC SELECT * FROM IotDeviceData;

# METADATA ********************

# META {
# META   "language": "sparksql"
# META }

# CELL ********************

