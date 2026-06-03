select

    customer_id,

    age,

    tenure,

    usage_frequency,

    support_calls,

    payment_delay,

    total_spend,

    avg_monthly_spend,

    engagement_score,

    is_high_support,

    is_late_payer,

    churn

from {{ ref('stg_customer_churn') }}