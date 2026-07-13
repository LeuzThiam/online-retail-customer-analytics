-- Tables de dimensions du modèle en étoile (MySQL 8.0+).

CREATE TABLE dim_country (
    country_key         INT AUTO_INCREMENT PRIMARY KEY,
    country_name         VARCHAR(100) NOT NULL UNIQUE,
    iso2_code            CHAR(2),
    iso3_code            CHAR(3),
    region               VARCHAR(100),
    is_united_kingdom    BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE dim_product (
    product_key          INT AUTO_INCREMENT PRIMARY KEY,
    stock_code            VARCHAR(20) NOT NULL UNIQUE,
    product_description   VARCHAR(255),
    product_type          VARCHAR(50) DEFAULT 'merchandise'
);

CREATE TABLE dim_customer (
    customer_key          INT AUTO_INCREMENT PRIMARY KEY,
    customer_id            DECIMAL(10, 0) NOT NULL UNIQUE,
    country_key            INT,
    first_purchase_date     DATETIME,
    last_purchase_date      DATETIME,
    customer_status          VARCHAR(50),  -- rempli lors de la segmentation RFM (Phase 6)
    FOREIGN KEY (country_key) REFERENCES dim_country(country_key)
);

-- Grain horaire : une ligne par heure, pour permettre l'analyse par jour
-- ET par heure sans dimension "temps" séparée.
CREATE TABLE dim_date (
    date_key             INT AUTO_INCREMENT PRIMARY KEY,
    full_date             DATE NOT NULL,
    year                  INT NOT NULL,
    quarter               INT NOT NULL,
    month                 INT NOT NULL,
    month_name            VARCHAR(20) NOT NULL,
    week                  INT NOT NULL,
    day                   INT NOT NULL,
    day_name              VARCHAR(20) NOT NULL,
    hour                  INT NOT NULL,
    is_weekend            BOOLEAN NOT NULL,
    is_complete_month     BOOLEAN NOT NULL,
    UNIQUE KEY uk_date_hour (full_date, hour)
);

CREATE TABLE dim_transaction_type (
    transaction_type_key   INT AUTO_INCREMENT PRIMARY KEY,
    transaction_type        VARCHAR(30) NOT NULL UNIQUE,
    is_sale                  BOOLEAN NOT NULL DEFAULT FALSE,
    is_cancellation           BOOLEAN NOT NULL DEFAULT FALSE,
    is_adjustment              BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE dim_source (
    source_key            INT AUTO_INCREMENT PRIMARY KEY,
    dataset_name            VARCHAR(100) NOT NULL,
    sheet_name               VARCHAR(50),
    source_url                VARCHAR(255),
    download_date              DATE
);
