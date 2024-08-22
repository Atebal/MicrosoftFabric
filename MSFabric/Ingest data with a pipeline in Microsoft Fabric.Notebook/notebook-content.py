# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "f22dcaa6-2768-4b0c-9cff-19d473724a14",
# META       "default_lakehouse_name": "MyLakeHouse",
# META       "default_lakehouse_workspace_id": "1bb8e816-a170-468a-959f-db273b471f1b",
# META       "known_lakehouses": [
# META         {
# META           "id": "f22dcaa6-2768-4b0c-9cff-19d473724a14"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

table_name="sales"

# CELL ********************

from pyspark.sql.functions import *
from pyspark.sql.types import *

schema=StructType(
    [
         StructField('SalesOrderNumber', StringType(), True),
         StructField('SalesOrderLineNumber', IntegerType(), True), 
         StructField('OrderDate', DateType(), True), 
         StructField('CustomerName', StringType(), True), 
         StructField('EmailAddress', StringType(), True), 
         StructField('Item', StringType(), True), 
         StructField('Quantity', IntegerType(), True), 
         StructField('UnitPrice', FloatType(), True), 
         StructField('TaxAmount', FloatType(), True)
         ])

df=spark.read.format("csv").schema(schema).option("header","true").load("Files/new_data/*.csv")

df=df.withColumn("Year",year(col("OrderDate"))).withColumn("Month",month(col("OrderDate")))

df=df.withColumn("FirstName",split(col("CustomerName")," ").getItem(0)).withColumn("LastName",split(col("CustomerName")," ").getItem(1))

df = df["SalesOrderNumber", "SalesOrderLineNumber", "OrderDate", "Year", "Month", "FirstName", "LastName", "EmailAddress", "Item", "Quantity", "UnitPrice", "TaxAmount"]

df.write.format("delta").mode("append").saveAsTable(table_name)

