{{ config(materialized='table') }}

with base as (

    select
        customer_id,
        signup_date,
        monthly_charges,
        churned,

        floor(datediff(last_activity_date, signup_date) / 30) as tenure_months

    from {{ ref('dim_customers') }}

),

features as (

    select
        customer_id,
        tenure_months,
        monthly_charges,
        churned,

        case
            when tenure_months < 6 then 'new'
            when tenure_months < 24 then 'established'
            else 'loyal'
        end as tenure_bucket,

        case
            when monthly_charges >= 80 then 1
            else 0
        end as is_high_value

    from base

)

select * from features
