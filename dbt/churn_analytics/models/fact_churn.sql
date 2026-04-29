{{ config(materialized='table') }}

SELECT
    customer_id,
    churned,
    monthly_charges,
    datediff(last_activity_date, signup_date) AS customer_tenure_days
FROM {{ ref('dim_customers') }}
