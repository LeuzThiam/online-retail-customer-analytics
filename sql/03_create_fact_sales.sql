-- Table de faits : une ligne par ligne de transaction (grain = ligne de facture).

CREATE TABLE fact_sales (
    sales_key                INT AUTO_INCREMENT PRIMARY KEY,
    invoice_no                 VARCHAR(20) NOT NULL,
    date_key                     INT NOT NULL,
    customer_key                  INT,  -- NULL si client inconnu
    product_key                    INT NOT NULL,
    country_key                     INT NOT NULL,
    transaction_type_key              INT NOT NULL,
    source_key                          INT,
    quantity                              INT NOT NULL,
    unit_price                             DECIMAL(12, 2) NOT NULL,
    gross_line_value                        DECIMAL(14, 2) NOT NULL,
    cancelled_line_value                     DECIMAL(14, 2) NOT NULL,
    net_line_value                            DECIMAL(14, 2) NOT NULL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (country_key) REFERENCES dim_country(country_key),
    FOREIGN KEY (transaction_type_key) REFERENCES dim_transaction_type(transaction_type_key),
    FOREIGN KEY (source_key) REFERENCES dim_source(source_key)
);

CREATE INDEX idx_fact_sales_date ON fact_sales(date_key);
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_key);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_key);
CREATE INDEX idx_fact_sales_country ON fact_sales(country_key);
