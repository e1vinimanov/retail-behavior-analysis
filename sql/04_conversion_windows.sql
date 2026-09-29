CREATE OR REPLACE VIEW conversion_windows AS
WITH eligible_carts AS (
    SELECT client_id, sku, MIN(timestamp) AS first_cart_time
    FROM cart_events
    GROUP BY client_id, sku
    HAVING MIN(timestamp) < TIMESTAMP '2022-12-01 00:00:00'
),
cart_outcomes AS (
    SELECT c.client_id, c.sku, c.first_cart_time,
           MIN(p.timestamp) AS first_purchase_after_cart
    FROM eligible_carts AS c
    LEFT JOIN purchase_events AS p
        ON p.client_id = c.client_id
        AND p.sku = c.sku
        AND p.timestamp > c.first_cart_time
        AND p.timestamp <= c.first_cart_time + INTERVAL '7 days'
    GROUP BY c.client_id, c.sku, c.first_cart_time
)
SELECT COUNT(*) AS eligible_pairs,
       COUNT(*) FILTER (
           WHERE first_purchase_after_cart <= first_cart_time + INTERVAL '1 day'
       ) AS converted_1d,
       COUNT(*) FILTER (
           WHERE first_purchase_after_cart <= first_cart_time + INTERVAL '3 days'
       ) AS converted_3d,
       COUNT(first_purchase_after_cart) AS converted_7d
FROM cart_outcomes;

SELECT * FROM conversion_windows;
