-- Requêtes d'analyse des produits.

-- Meilleurs produits par chiffre d'affaires net.
SELECT
    p.stock_code,
    p.product_description,
    SUM(f.quantity) AS net_quantity,
    SUM(f.net_line_value) AS net_revenue
FROM fact_sales AS f
JOIN dim_product AS p ON f.product_key = p.product_key
GROUP BY p.stock_code, p.product_description
ORDER BY net_revenue DESC
LIMIT 20;

-- Produits avec le taux d'annulation le plus élevé (volume brut significatif).
SELECT
    p.stock_code,
    p.product_description,
    SUM(f.gross_line_value) AS gross_value,
    SUM(f.cancelled_line_value) AS cancelled_value,
    SUM(f.cancelled_line_value)
        / NULLIF(SUM(f.gross_line_value), 0) AS cancellation_rate
FROM fact_sales AS f
JOIN dim_product AS p ON f.product_key = p.product_key
GROUP BY p.stock_code, p.product_description
HAVING SUM(f.gross_line_value) > 100
ORDER BY cancellation_rate DESC
LIMIT 20;
