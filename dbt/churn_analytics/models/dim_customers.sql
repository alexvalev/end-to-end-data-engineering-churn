{{ config(materialized='table') }}

SELECT
    customer_id,
    signup_date,
    last_activity_date,
    monthly_charges,
    churned
FROM {{ source('silver', 'silver_customers') }}
