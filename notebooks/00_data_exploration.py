# Databricks notebook source
# MAGIC %md
# MAGIC # Data Exploration

# COMMAND ----------

#Loading in the dataset and infering schema
df_train = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("/Volumes/workspace/default/data_engineering_project/customer_churn_train.csv")
)

display(df_train)

# COMMAND ----------

#Displaying schema
df_train.printSchema()

# COMMAND ----------

df_train.count()

# COMMAND ----------

#Counting missing values in each column
from pyspark.sql.functions import col, count, when

missing_df = df_train.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in df_train.columns
])

display(missing_df)

# COMMAND ----------

#Checking for duplicates
if df_train.count() > df_train.dropDuplicates(df_train.columns).count():
    raise ValueError('Data has duplicates')


# COMMAND ----------

#Inspecting churn values
display(
    df_train.groupBy("Churn").count()
)