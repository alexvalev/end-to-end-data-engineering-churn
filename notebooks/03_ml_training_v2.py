# Databricks notebook source
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier

import mlflow
import mlflow.spark

# COMMAND ----------

# MAGIC %md
# MAGIC # Logicstic Regression

# COMMAND ----------

import os

os.environ["MLFLOW_DFS_TMP"] = (
    "/Volumes/workspace/default/data_engineering_project/mlflow_tmp"
)

# COMMAND ----------

#Load in dataset
df = spark.table(
    "workspace.dbt_churn_analytics.gold_churn_features"
)

display(df)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df.columns

# COMMAND ----------

display(df.groupBy("churn").count())

# COMMAND ----------

#Assemble features
feature_columns = [
    "age",
    "tenure",
    "usage_frequency",
    "support_calls",
    "payment_delay",
    "total_spend",
    "avg_monthly_spend",
    "engagement_score",
    "is_high_support",
    "is_late_payer"
]

assembler = VectorAssembler(
    inputCols=feature_columns,
    outputCol="features"
)

df_features = assembler.transform(df)

# COMMAND ----------

#Split into data train and test sets
train_df, test_df = df_features.randomSplit(
    [0.8, 0.2],
    seed=42
)

# COMMAND ----------

#Train logistic regression model
lr = LogisticRegression(
    featuresCol="features",
    labelCol="churn"
)

lr_model = lr.fit(train_df)

# COMMAND ----------

#Predict on test set
lr_predictions = lr_model.transform(test_df)

display(
    lr_predictions.select(
        "customer_id",
        "churn",
        "prediction",
        "probability"
    )
)

# COMMAND ----------

#Evaluate results using AUC
evaluator = BinaryClassificationEvaluator(
    labelCol="churn"
)

lr_auc = evaluator.evaluate(lr_predictions)

print(f"AUC = {lr_auc:.4f}")

# COMMAND ----------

#Log model to MLflow
with mlflow.start_run(run_name="logistic_regression_v2"):

    mlflow.log_param(
        "model_type",
        "logistic_regression"
    )

    mlflow.log_metric(
        "auc",
        lr_auc
    )

    mlflow.spark.log_model(
        lr_model,
        "model"
    )

# COMMAND ----------

#Check coefficients
coefficients = list(zip(
    feature_columns,
    lr_model.coefficients.toArray()
))

sorted(
    coefficients,
    key=lambda x: abs(x[1]),
    reverse=True
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Random Forest

# COMMAND ----------

rf = RandomForestClassifier(
    featuresCol="features",
    labelCol="churn",
    numTrees=100,
    seed=42
)

rf_model = rf.fit(train_df)

# COMMAND ----------

rf_predictions = rf_model.transform(test_df)

# COMMAND ----------

rf_auc = evaluator.evaluate(rf_predictions)

print(f"Random Forest AUC = {rf_auc:.4f}")

# COMMAND ----------

with mlflow.start_run(run_name="random_forest_v2"):

    mlflow.log_param("model_type", "random_forest")
    mlflow.log_param("num_trees", 100)

    mlflow.log_metric("auc", rf_auc)

    mlflow.spark.log_model(
        spark_model=rf_model,
        artifact_path="model",
        dfs_tmpdir="/Volumes/workspace/default/data_engineering_project/mlflow_tmp"
    )

# COMMAND ----------

feature_importances = list(zip(
    feature_columns,
    rf_model.featureImportances.toArray()
))

sorted(
    feature_importances,
    key=lambda x: x[1],
    reverse=True
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Training on the whole training set and predicting on the test set

# COMMAND ----------

test_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(
        "/Volumes/workspace/default/data_engineering_project/customer_churn_test.csv"
    )
)

test_df.printSchema()

# COMMAND ----------

print(test_df.count())

# COMMAND ----------

test_df2 = test_df.dropna()

test_df2 = test_df2.dropDuplicates()

print(test_df2.count())

# COMMAND ----------

from pyspark.sql.functions import col, when, round

test_features = (
    test_df
    .withColumn(
        "avg_monthly_spend",
        round(col("Total Spend") / col("Tenure"), 2)
    )
    .withColumn(
        "engagement_score",
        round(
            col("Usage Frequency") / (col("Support Calls") + 1),
            2
        )
    )
    .withColumn(
        "is_high_support",
        when(col("Support Calls") >= 5, 1).otherwise(0)
    )
    .withColumn(
        "is_late_payer",
        when(col("Payment Delay") > 10, 1).otherwise(0)
    )
)

# COMMAND ----------

test_features = (
    test_features
    .withColumnRenamed("CustomerID", "customer_id")
    .withColumnRenamed("Age", "age")
    .withColumnRenamed("Tenure", "tenure")
    .withColumnRenamed("Usage Frequency", "usage_frequency")
    .withColumnRenamed("Support Calls", "support_calls")
    .withColumnRenamed("Payment Delay", "payment_delay")
    .withColumnRenamed("Total Spend", "total_spend")
    .withColumnRenamed("Churn", "churn")
)

# COMMAND ----------

test_features = assembler.transform(test_features)

# COMMAND ----------

final_rf_model = rf.fit(df_features)

# COMMAND ----------

final_rf_model = rf.fit(train_df)

# COMMAND ----------

final_rf_predictions = final_rf_model.transform(test_features)

# COMMAND ----------

final_rf_auc = evaluator.evaluate(final_rf_predictions)

print(f"Final Holdout AUC = {final_rf_auc:.4f}")

# COMMAND ----------

(
    final_rf_predictions
    .select(
        "customer_id",
        "prediction",
        "probability"
    )
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(
        "workspace.dbt_churn_analytics.churn_predictions"
    )
)

# COMMAND ----------

display(
    spark.table(
        "workspace.dbt_churn_analytics.churn_predictions"
    )
)

# COMMAND ----------

final_lr_model = lr.fit(df_features)
final_lr_predictions = final_lr_model.transform(test_features)
final_lr_auc = evaluator.evaluate(final_lr_predictions)
print(final_lr_auc)

# COMMAND ----------

#Log model to MLflow
with mlflow.start_run(run_name="logistic_regression_v2"):

    mlflow.log_param(
        "model_type",
        "logistic_regression"
    )

    mlflow.log_metric(
        "auc",
        final_lr_auc
    )

    mlflow.spark.log_model(
        final_lr_model,
        "model"
    )