-- Databricks notebook source
CREATE OR REPLACE TABLE fact_customer_metrics AS
SELECT
  customer_id,
  DATE_DIFF(last_activity_date, signup_date) AS customer_lifetime_days,
  DATE_DIFF(CURRENT_DATE(), last_activity_date) AS days_since_last_activity,
  churned
FROM silver_customers;

-- COMMAND ----------

SELECT
  COUNT (*) AS total_rows,
  SUM(churned) AS churned_customers
FROM fact_customer_metrics

-- COMMAND ----------

SELECT * FROM fact_customer_metrics

-- COMMAND ----------

