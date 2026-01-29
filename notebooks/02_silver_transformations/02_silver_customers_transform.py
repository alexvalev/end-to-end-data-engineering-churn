# Databricks notebook source
from pyspark.sql.functions import col, to_date

# COMMAND ----------

df_bronze = spark.table("bronze_customers")
df_bronze.display()


# COMMAND ----------

df_silver = (
    df_bronze
    .withColumn('signup_date', to_date(col('signup_date')))
    .withColumn('last_activity_date', to_date(col('last_activity_date')))
    .withColumn('churned', col('churned').cast('int'))
    .withColumn('monthly_charges', col('monthly_charges').cast('double'))
    .dropDuplicates(['customer_id'])
)

# COMMAND ----------

(
    df_silver.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("silver_customers")
)


# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_customers,
# MAGIC     SUM(churned) AS churned_customers
# MAGIC FROM silver_customers;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_rows,
# MAGIC     COUNT(DISTINCT customer_id) AS unique_customers
# MAGIC FROM silver_customers;
# MAGIC

# COMMAND ----------

