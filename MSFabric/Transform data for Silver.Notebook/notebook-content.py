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

# MARKDOWN ********************

# **Transform data for Silver**


# CELL ********************

from pyspark.sql.types import *

#create the schema for the table

orderSchema=StructType([
    StructField("SalesOrderNumber",StringType()),
    StructField("SalesOrderLineNumber",IntegerType()),
    StructField("OrderDate",DateType()),
    StructField("CustomerName",StringType()),
    StructField("Email",StringType()),
    StructField("Item",StringType()),
    StructField("Quantity",IntegerType()),
    StructField("UnitPrice",FloatType()),
    StructField("Tax",FloatType())
])

df=spark.read.format("csv").option("header","true").schema(orderSchema).load("Files/bronze/*.csv")

display(df.head(10))

# CELL ********************

from pyspark.sql.functions import when,lit,col,current_timestamp,input_file_name

df=df.withColumn("FileName",input_file_name()) \
      .withColumn("IsFlagged",when(col("orderDate")<'2019-08-01',True).otherwise(False)) \
      .withColumn("CreatedTS",current_timestamp()).withColumn("ModifiedTS",current_timestamp())


df=df.withColumn("customerName", when((col("customerName").isNull() | (col("customerName")=="")),lit("Unknown")).otherwise(col("CustomerName")))

# CELL ********************


from pyspark.sql.types import *
from delta.tables import *



DeltaTable.createIfNotExists(spark) \
    .tableName("sales_silver") \
    .addColumn("SalesOrderNumber",StringType()) \
    .addColumn("SalesOrderLineNumber",IntegerType()) \
    .addColumn("OrderDate",DateType()) \
    .addColumn("CustomerName",StringType()) \
    .addColumn("Email",StringType()) \
    .addColumn("Item",StringType()) \
    .addColumn("Quantity",IntegerType()) \
    .addColumn("UnitPrice",FloatType()) \
    .addColumn("Tax",FloatType()) \
    .addColumn("FileName", StringType()) \
    .addColumn("IsFlagged", BooleanType()) \
    .addColumn("CreatedTS", DateType()) \
    .addColumn("ModifiedTS", DateType()) \
    .execute()

# CELL ********************

from delta.tables import *

deltaTable=DeltaTable.forPath(spark,'Tables/sales_silver')

dfUpdates=df

deltaTable.alias('silver') \
    .merge(
        dfUpdates.alias('updates'),
        'silver.SalesOrderNumber = updates.SalesOrderNumber and silver.OrderDate = updates.OrderDate and silver.CustomerName = updates.CustomerName and silver.Item = updates.Item'
         ) \
    .whenMatchedUpdate( set=
        {

        }
        ) \
    .whenNotMatchedInsert(values=
    {
        "SalesOrderNumber": "updates.SalesOrderNumber",
      "SalesOrderLineNumber": "updates.SalesOrderLineNumber",
      "OrderDate": "updates.OrderDate",
      "CustomerName": "updates.CustomerName",
      "Email": "updates.Email",
      "Item": "updates.Item",
      "Quantity": "updates.Quantity",
      "UnitPrice": "updates.UnitPrice",
      "Tax": "updates.Tax",
      "FileName": "updates.FileName",
      "IsFlagged": "updates.IsFlagged",
      "CreatedTS": "updates.CreatedTS",
      "ModifiedTS": "updates.ModifiedTS"
    }
    ) \
    .execute()

# CELL ********************

