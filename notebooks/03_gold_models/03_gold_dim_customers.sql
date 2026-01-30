-- Databricks notebook source
CREATE OR REPLACE TABLE dim_customers AS
SELECT
  customer_id,
  signup_date,
  last_activity_date,
  monthly_charges,
  churned
FROM silver_customers;

-- COMMAND ----------

SELECT
    COUNT(*) AS total_customers,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM dim_customers;


-- COMMAND ----------

SELECT * FROM dim_customers;


-- COMMAND ----------

