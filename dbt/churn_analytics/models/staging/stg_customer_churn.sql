select *

from {{ source('churn_analytics', 'silver_customer_churn') }}