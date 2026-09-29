CREATE OR REPLACE VIEW monthly_repeat_purchase AS
WITH eligible_customer AS (
    SELECT client_id, MIN(timestamp::date) AS first_purchase_day
    FROM purchase_events
    GROUP BY client_id
    HAVING MIN(timestamp::date) <= DATE '2022-11-07'
),
customer_returns AS (
    SELECT e.client_id, e.first_purchase_day,
           MIN(p.timestamp::date) AS first_return_day
    FROM eligible_customer AS e
    LEFT JOIN purchase_events AS p
        ON p.client_id = e.client_id
        AND p.timestamp::date > e.first_purchase_day
        AND p.timestamp::date <= e.first_purchase_day + 30
    GROUP BY e.client_id, e.first_purchase_day
)
SELECT DATE_TRUNC('month', first_purchase_day)::date AS cohort_month,
       COUNT(*) AS eligible_customers,
       COUNT(first_return_day) AS returned_within_30_days,
       ROUND(100.0 * COUNT(first_return_day) / NULLIF(COUNT(*), 0), 2) AS return_percentage
FROM customer_returns
GROUP BY DATE_TRUNC('month', first_purchase_day)::date;

SELECT * FROM monthly_repeat_purchase ORDER BY cohort_month;
