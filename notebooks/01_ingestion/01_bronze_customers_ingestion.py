# Databricks notebook source
file_path = '/Volumes/workspace/default/data_engineering_project/customers.csv'

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(file_path)
)

df.display()

# COMMAND ----------

df.printSchema()

# COMMAND ----------

(
    df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("bronze_customers")
)


# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bronze_customers;
# MAGIC