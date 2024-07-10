CREATE SCHEMA sale;

CREATE TABLE IF NOT EXISTS shopsmartdb.sale.transactions (
    transaction_id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    product_id VARCHAR(255) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    price DOUBLE PRECISION NOT NULL,
	total_amount DOUBLE PRECISION NOT NULL,
	transaction_date TIMESTAMPTZ NOT NULL,
	created_date TIMESTAMPTZ NOT NULL
);