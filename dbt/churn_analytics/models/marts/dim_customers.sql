select
    customer_id,
    age,
    gender,
    subscription_type,
    contract_length

from {{ ref('stg_customer_churn') }}