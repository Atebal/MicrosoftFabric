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

# Welcome to your new notebook
# Type here in the cell editor to add code!


# CELL ********************

df = spark.read.format("csv").option("header","true").load("Files/orders/2019.csv")
# df now is a Spark DataFrame containing CSV data from "Files/orders/2019.csv".
display(df)

# CELL ********************

df=spark.read.format("csv").option("header","false").load("Files/orders/2019.csv")
display(df);


# CELL ********************

from pyspark.sql.types import *;

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
]
)

 df=spark.read.format("CSV").schema(orderSchema).load("Files/orders/2019.csv");
 display(df);

# CELL ********************


from pyspark.sql.types import *;

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
]
);
df=spark.read.format("CSV").schema(orderSchema).load("Files/orders/*.csv");
#display(df);

# CELL ********************


customers=df['CustomerName', 'Email']
print(customers.count())
print(customers.distinct().count())
display(customers.distinct())

# CELL ********************

customers=df.select('CustomerName', 'Email')
print(customers.count())
print(customers.distinct().count())
display(customers.distinct())

# CELL ********************

productsales=df.select("Item", "Quantity").groupBy("Item").sum()
display(productsales)

# CELL ********************

from pyspark.sql.functions import *
yearlySales=df.select(year(col('OrderDate')).alias('Year')).groupBy('Year').count().orderBy('Year')
display(yearlySales)

# CELL ********************

from pyspark.sql.functions import *

transformed_df=df.withColumn("Year",year(col("OrderDate"))).withColumn("Month",month(col("OrderDate")))
transformed_df=transformed_df.withColumn("FirstName",split(col("CustomerName")," ").getItem(0)).withColumn("LastName",split(col("CustomerName")," ").getItem(1))
transformed_df=transformed_df["SalesOrderNumber", "SalesOrderLineNumber", "OrderDate", "Year", "Month", "FirstName", "LastName", "Email", "Item", "Quantity", "UnitPrice", "Tax"]
display(transformed_df.limit(5));

# CELL ********************

transformed_df.write.mode('overwrite').parquet('Files/transformed_data/orders')
print("Transformed data saved!")

# CELL ********************

orders_df=spark.read.format('parquet').load("Files/transformed_data/orders")
display(orders_df)

# CELL ********************

orders_df.write.partitionBy("Year","Month").mode("overwrite").parquet("Files/partitioned_data")
print("Transformed data saved!")

# CELL ********************

orders_2021_df=spark.read.format('parquet').load("Files/partitioned_data/Year=2021/Month=*")
display(orders_2021_df)

# CELL ********************

df.write.format('delta').saveAsTable("salesorders")

# CELL ********************

spark.sql("Describe EXTENDED salesorders").show(truncate=False)

# CELL ********************


# CELL ********************

df = spark.sql("SELECT * FROM MyLakeHouse.salesorders LIMIT 1000")
display(df)

# CELL ********************

# MAGIC %%sql
# MAGIC select YEAR(OrderDate) as orderYear,
# MAGIC SUM((UnitPrice * Quantity) + Tax) AS GrossRevenue
# MAGIC FROM salesorders
# MAGIC GROUP BY YEAR(OrderDate)
# MAGIC ORDER BY OrderYear;

# METADATA ********************

# META {
# META   "language": "sparksql"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * FROM salesorders

# METADATA ********************

# META {
# META   "language": "sparksql"
# META }

# CELL ********************

sqlQuery="SELECT CAST(YEAR(OrderDate) AS CHAR(4)) AS OrderYear, \
            SUM((UnitPrice * Quantity) + Tax) AS GrossRevenue \
            FROM salesorders \
            GROUP BY CAST(YEAR(OrderDate) AS CHAR(4)) \
            ORDER BY OrderYear"
df_spark=spark.sql(sqlQuery)
display(df_spark)

# CELL ********************

from matplotlib import pyplot as plt

plt.clf()
df_sales = df_spark.toPandas()
plt.bar(x=df_sales['OrderYear'],height=df_sales['GrossRevenue'],color='orange')
plt.title('Revenue by Year')
plt.xlabel('Year')
plt.ylabel('Revenue')
plt.grid(color='#95a5a6',linestyle='--',linewidth=2,axis='y',alpha=0.7)
plt.xticks(rotation=45)

plt.show()

# CELL ********************

from matplotlib import pyplot   as plt

plt.clf()

fig=plt.figure(figsize=(8,3))
plt.bar(x=df_sales['OrderYear'],height=df_sales['GrossRevenue'],color='orange')

plt.title('Revenue by Year')
plt.xlabel('Year')
plt.ylabel('Revenue')
plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
plt.xticks(rotation=45)

# Show the figure
plt.show()

# CELL ********************

from matplotlib import pyplot as plt 

plt.clf()

fig,ax=plt.subplots(1,2,figsize=(10,4))
ax[0].bar(x=df_sales['OrderYear'], height=df_sales['GrossRevenue'], color='orange')
ax[0].set_title('Revenue by Year')


yearly_counts=df_sales['OrderYear'].value_counts()
ax[1].pie(yearly_counts)
ax[1].set_title('Orders per Year')
ax[1].legend(yearly_counts.keys().tolist())

fig.suptitle('Sales Data')
plt.show()



# CELL ********************

import seaborn as sns   

plt.clf()

#sns.set_theme(style="none")
ax=sns.barplot(x="OrderYear", y="GrossRevenue", data=df_sales)

plt.show()


# CELL ********************

import seaborn as sns   

plt.clf()

sns.set_theme(style="whitegrid")
ax=sns.barplot(x="OrderYear", y="GrossRevenue", data=df_sales)

plt.show()

# CELL ********************

import seaborn as sns

# Clear the plot area
plt.clf()

# Create a line chart
ax = sns.lineplot(x="OrderYear", y="GrossRevenue", data=df_sales)
plt.show()

# CELL ********************

