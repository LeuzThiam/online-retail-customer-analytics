-- Chargement des données depuis l'export Python (data/processed/transactions_clean.csv)
-- produit par notebooks/03_transaction_cleaning.ipynb.
-- Nécessite MySQL 8.0+ (CTE récursive) et 8.0.14+ (LATERAL).

-- 1. Table de transit (staging), même structure que le CSV exporté.
CREATE TABLE staging_transactions (
    invoice_no          VARCHAR(20),
    stock_code            VARCHAR(20),
    description            VARCHAR(255),
    quantity                 INT,
    invoice_date               DATETIME,
    unit_price                  DECIMAL(12, 2),
    customer_id                  DECIMAL(10, 0),
    country                       VARCHAR(100),
    is_cancellation                 BOOLEAN,
    transaction_type                 VARCHAR(30),
    description_clean                  VARCHAR(255),
    country_clean                        VARCHAR(100),
    quantity_outlier                       BOOLEAN,
    line_revenue                            DECIMAL(14, 2)
);

-- 2. Import du CSV. LOAD DATA LOCAL nécessite local_infile activé :
--   côté serveur : SET GLOBAL local_infile = 1;
--   côté client  : se connecter avec `mysql --local-infile=1 ...`
--                  (ou OPT_LOCAL_INFILE=1 dans les options avancées de Workbench)
-- Adapter le chemin du fichier à votre machine.
--
-- Sur une machine aux ressources limitées, charger les 1M+ lignes complètes
-- peut être lent. Pour valider rapidement que tout le pipeline fonctionne,
-- utilisez d'abord data/processed/transactions_sample.csv (échantillon de
-- 50 000 lignes) à la place du fichier complet ci-dessous.

TRUNCATE TABLE staging_transactions;

LOAD DATA LOCAL INFILE 'C:\\Users\\modou\\OneDrive\\Documents\\COURS\\BacInformatiqueUQAR\\Revision\\DataAnalyst\\Python\\online-retail-customer-analytics\\data\\processed\\transactions_sample.csv'
INTO TABLE staging_transactions
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(invoice_no, stock_code, description, quantity, invoice_date, unit_price,
 @customer_id_raw, country, @is_cancellation_raw, transaction_type,
 description_clean, country_clean, @quantity_outlier_raw, line_revenue)
SET
    customer_id = NULLIF(@customer_id_raw, ''),
    is_cancellation = (@is_cancellation_raw = 'True'),
    quantity_outlier = (@quantity_outlier_raw = 'True');

-- 3. Peuplement des dimensions à partir des valeurs distinctes de la table de transit.

INSERT IGNORE INTO dim_country (country_name)
SELECT DISTINCT country_clean FROM staging_transactions
WHERE country_clean IS NOT NULL;

-- Une ligne par stock_code : ANY_VALUE() prend une description associée
-- (pas de DISTINCT ON en MySQL).
INSERT IGNORE INTO dim_product (stock_code, product_description)
SELECT stock_code, ANY_VALUE(description_clean)
FROM staging_transactions
GROUP BY stock_code;

INSERT IGNORE INTO dim_transaction_type (transaction_type, is_sale, is_cancellation, is_adjustment)
VALUES
    ('sale', TRUE, FALSE, FALSE),
    ('cancellation', FALSE, TRUE, FALSE),
    ('negative_adjustment', FALSE, FALSE, TRUE),
    ('zero_quantity', FALSE, FALSE, TRUE);

-- dim_date à grain horaire : calendrier généré par CTE récursive.
-- Le nombre de lignes (~17 500) dépasse la limite par défaut de récursion :
-- augmenter cte_max_recursion_depth avant d'exécuter cette requête.
SET SESSION cte_max_recursion_depth = 20000;

INSERT INTO dim_date (
    full_date, year, quarter, month, month_name, week, day, day_name, hour,
    is_weekend, is_complete_month
)
WITH RECURSIVE calendrier AS (
    SELECT TIMESTAMP('2009-12-01 00:00:00') AS d
    UNION ALL
    SELECT d + INTERVAL 1 HOUR
    FROM calendrier
    WHERE d < TIMESTAMP('2011-12-09 23:00:00')
)
SELECT
    DATE(d),
    YEAR(d),
    QUARTER(d),
    MONTH(d),
    DATE_FORMAT(d, '%M'),
    WEEK(d, 3),
    DAY(d),
    DATE_FORMAT(d, '%W'),
    HOUR(d),
    WEEKDAY(d) IN (5, 6),
    NOT (YEAR(d) = 2011 AND MONTH(d) = 12)
FROM calendrier;

-- dim_customer : pays "principal" approximé par le pays le plus fréquent pour
-- ce client (un client change rarement de pays, mais ce n'est pas garanti).
--
-- Version en une seule passe (ROW_NUMBER) plutôt qu'un LATERAL corrélé :
-- LATERAL relançait une recherche séparée pour chacun des ~4 300 clients
-- (beaucoup trop lent sur 1M de lignes, même indexé). Ici, une seule
-- agrégation GROUP BY (customer_id, country_clean) calcule tous les comptages
-- d'un coup, puis ROW_NUMBER() garde le pays le plus fréquent par client.
INSERT IGNORE INTO dim_customer (customer_id, country_key, first_purchase_date, last_purchase_date)
SELECT
    dates_client.customer_id,
    dc.country_key,
    dates_client.first_purchase_date,
    dates_client.last_purchase_date
FROM (
    SELECT
        customer_id,
        MIN(invoice_date) AS first_purchase_date,
        MAX(invoice_date) AS last_purchase_date
    FROM staging_transactions
    WHERE customer_id IS NOT NULL
    GROUP BY customer_id
) AS dates_client
JOIN (
    SELECT customer_id, country_clean
    FROM (
        SELECT
            customer_id,
            country_clean,
            COUNT(*) AS nb_lignes,
            ROW_NUMBER() OVER (
                PARTITION BY customer_id ORDER BY COUNT(*) DESC
            ) AS rang
        FROM staging_transactions
        WHERE customer_id IS NOT NULL
        GROUP BY customer_id, country_clean
    ) AS classement
    WHERE rang = 1
) AS pays_principal
    ON pays_principal.customer_id = dates_client.customer_id
JOIN dim_country dc ON dc.country_name = pays_principal.country_clean;

-- 4. Peuplement de la table de faits.
INSERT INTO fact_sales (
    invoice_no, date_key, customer_key, product_key, country_key,
    transaction_type_key, quantity, unit_price,
    gross_line_value, cancelled_line_value, net_line_value
)
SELECT
    s.invoice_no,
    dd.date_key,
    dcu.customer_key,
    dp.product_key,
    dco.country_key,
    dtt.transaction_type_key,
    s.quantity,
    s.unit_price,
    GREATEST(s.line_revenue, 0),
    GREATEST(-s.line_revenue, 0),
    s.line_revenue
FROM staging_transactions s
JOIN dim_date dd
    ON dd.full_date = DATE(s.invoice_date)
    AND dd.hour = HOUR(s.invoice_date)
LEFT JOIN dim_customer dcu ON dcu.customer_id = s.customer_id
JOIN dim_product dp ON dp.stock_code = s.stock_code
JOIN dim_country dco ON dco.country_name = s.country_clean
JOIN dim_transaction_type dtt ON dtt.transaction_type = s.transaction_type;
