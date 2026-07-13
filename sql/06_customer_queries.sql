-- Requêtes d'analyse des clients.

-- Meilleurs clients par chiffre d'affaires net.
SELECT
    c.customer_id,
    COUNT(DISTINCT f.invoice_no) AS number_of_orders,
    SUM(f.net_line_value) AS net_revenue
FROM fact_sales AS f
JOIN dim_customer AS c ON f.customer_key = c.customer_key
GROUP BY c.customer_id
ORDER BY net_revenue DESC
LIMIT 20;

-- Clients à achat unique (une seule commande valide).
WITH customer_orders AS (
    SELECT
        customer_key,
        COUNT(DISTINCT invoice_no) AS order_count
    FROM fact_sales
    WHERE net_line_value > 0
    GROUP BY customer_key
)
SELECT COUNT(*) AS one_time_customers
FROM customer_orders
WHERE order_count = 1;

-- Clients récemment inactifs (aucun achat depuis plus de 90 jours avant
-- la dernière date connue du dataset).
WITH derniere_date AS (
    SELECT MAX(d.full_date) AS date_max
    FROM fact_sales f
    JOIN dim_date d ON f.date_key = d.date_key
)
SELECT
    c.customer_id,
    c.last_purchase_date,
    DATEDIFF(
        (SELECT date_max FROM derniere_date),
        DATE(c.last_purchase_date)
    ) AS jours_inactivite
FROM dim_customer c
WHERE DATE(c.last_purchase_date)
    < (SELECT date_max FROM derniere_date) - INTERVAL 90 DAY
ORDER BY jours_inactivite DESC;
