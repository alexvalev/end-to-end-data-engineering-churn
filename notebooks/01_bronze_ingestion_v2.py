# Databricks notebook source
df_train = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("/Volumes/workspace/default/data_engineering_project/customer_churn_train.csv")
)

# COMMAND ----------

clean_columns = [
    c.lower()
     .replace(" ", "_")
    for c in df_train.columns
]

df_train = df_train.toDF(*clean_columns)

display(df_train)

# COMMAND ----------

df_train = df_train.dropna()

df_train = df_train.dropDuplicates()

# COMMAND ----------

df_train.write.mode("overwrite").format("delta").saveAsTable(
    "workspace.churn_analytics.bronze_customer_churn_train"
)

# COMMAND ----------

spark.sql("""
SELECT COUNT(*)
FROM workspace.churn_analytics.bronze_customer_churn_train
""").show()