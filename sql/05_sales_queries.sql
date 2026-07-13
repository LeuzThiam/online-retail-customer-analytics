-- Requêtes d'analyse des ventes.

-- Chiffre d'affaires mensuel (mois complets uniquement).
SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.net_line_value) AS net_revenue
FROM fact_sales AS f
JOIN dim_date AS d ON f.date_key = d.date_key
WHERE d.is_complete_month = TRUE
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- Ventes par jour de la semaine.
SELECT
    d.day_name,
    SUM(f.net_line_value) AS net_revenue
FROM fact_sales AS f
JOIN dim_date AS d ON f.date_key = d.date_key
GROUP BY d.day_name
ORDER BY net_revenue DESC;

-- Ventes par heure de la journée.
SELECT
    d.hour,
    SUM(f.net_line_value) AS net_revenue
FROM fact_sales AS f
JOIN dim_date AS d ON f.date_key = d.date_key
GROUP BY d.hour
ORDER BY d.hour;

-- Chiffre d'affaires et taux d'annulation par pays.
SELECT
    c.country_name,
    SUM(f.cancelled_line_value) AS cancelled_value,
    SUM(f.gross_line_value) AS gross_value,
    SUM(f.cancelled_line_value)
        / NULLIF(SUM(f.gross_line_value), 0) AS cancellation_rate
FROM fact_sales AS f
JOIN dim_country AS c ON f.country_key = c.country_key
GROUP BY c.country_name
ORDER BY cancellation_rate DESC;
