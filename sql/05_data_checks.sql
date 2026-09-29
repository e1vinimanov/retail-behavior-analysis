-- Run after import. Compare with reports/*_validation.md.
SELECT COUNT(*) AS purchase_events,
       COUNT(DISTINCT client_id) AS unique_buyers,
       MIN(timestamp) AS first_event,
       MAX(timestamp) AS last_event
FROM purchase_events;

SELECT COUNT(*) AS cart_events,
       COUNT(DISTINCT client_id) AS unique_cart_users,
       MIN(timestamp) AS first_event,
       MAX(timestamp) AS last_event
FROM cart_events;

-- Baseline across the observed period, without equal follow-up time.
WITH customer_activity AS (
    SELECT client_id, COUNT(DISTINCT timestamp::date) AS purchase_days
    FROM purchase_events
    GROUP BY client_id
)
SELECT COUNT(*) AS total_customers,
       COUNT(*) FILTER (WHERE purchase_days = 1) AS one_day_purchase,
       COUNT(*) FILTER (WHERE purchase_days >= 2) AS multiple_days_purchase,
       ROUND(100.0 * COUNT(*) FILTER (WHERE purchase_days >= 2)
             / NULLIF(COUNT(*), 0), 2) AS multiple_days_pct
FROM customer_activity;
