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

# Welcome to your new notebook
# Type here in the cell editor to add code!


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_fact_sale=spark.read.table("fact_sale")
df_dimension_date=spark.read.table("dimension_date")
df_dimension_city=spark.read.table("dimension_city")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

sale_by_date_city=df_fact_sale.alias("sale") \
.join(df_dimension_date.alias("date"), df_fact_sale.InvoiceDateKey== df_dimension_date.Date,"inner") \
.join(df_dimension_city.alias("city"),df_fact_sale.CityKey==df_dimension_city.CityKey,"inner") \
.select("date.Date", "date.CalendarMonthLabel", "date.Day", "date.ShortMonth", "date.CalendarYear", "city.City", "city.StateProvince", "city.SalesTerritory", "sale.TotalExcludingTax", "sale.TaxAmount", "sale.TotalIncludingTax", "sale.Profit") \
.groupBy("date.Date", "date.CalendarMonthLabel", "date.Day", "date.ShortMonth", "date.CalendarYear", "city.City", "city.StateProvince", "city.SalesTerritory") \
.sum("sale.TotalExcludingTax", "sale.TaxAmount", "sale.TotalIncludingTax", "sale.Profit") \
.withColumnRenamed("sum(TotalExcludingTax)","SumOfTotalExcludingTax") \
.withColumnRenamed("sum(TaxAmount)","SumOfTaxAmount") \
.withColumnRenamed("sum(TotalIncludingTax)","SumOfTotalIncludingTax") \
.withColumnRenamed("sum(Profit)","SumOfProfit") \
.orderBy("date.Date","city.StateProvince","city.city")

sale_by_date_city.write.mode("overwrite").format("delta").option("overwritSchema","true").save("Tables/aggregate_sale_by_date_city")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
