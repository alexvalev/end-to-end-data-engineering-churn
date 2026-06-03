# Databricks notebook source
df_bronze = spark.table(
    "workspace.churn_analytics.bronze_customer_churn_train"
)

display(df_bronze)

# COMMAND ----------

from pyspark.sql.functions import (
    col,
    when,
    round
)

df_silver = (
    df_bronze

    # rename key
    .withColumnRenamed("customerid", "customer_id")

    # standardize categorical columns
    .withColumn(
        "gender",
        when(col("gender") == "Male", "male")
        .otherwise("female")
    )

    .withColumn(
        "subscription_type",
        col("subscription_type")
    )

    .withColumn(
        "contract_length",
        col("contract_length")
    )

    # engineered columns
    .withColumn(
        "avg_monthly_spend",
        round(col("total_spend") / col("tenure"), 2)
    )

    .withColumn(
        "is_high_support",
        when(col("support_calls") >= 5, 1).otherwise(0)
    )

    .withColumn(
        "is_late_payer",
        when(col("payment_delay") >= 10, 1).otherwise(0)
    )

    .withColumn(
        "engagement_score",
        round(col("usage_frequency") / col("tenure"), 2)
    )
)

# COMMAND ----------

display(df_silver)

# COMMAND ----------

df_silver.write.mode("overwrite").format("delta").saveAsTable(
    "workspace.churn_analytics.silver_customer_churn"
)

# COMMAND ----------

