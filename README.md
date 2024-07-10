# ShopSmart Data Pipeline

This project sets up a data pipeline for a fictional e-commerce company "ShopSmart". The pipeline ingests, processes, and stores data from various sources to analyze customer behavior, sales performance, and inventory management.

## Project Structure

- `docker-compose.yml`: Docker Compose file to set up PostgreSQL and Spark services.
- `Dockerfile`: Dockerfile to build the Spark container with necessary dependencies.
- `db_init/init.sql`: SQL script to initialize the PostgreSQL database.
- `etl/etl_script.py`: ETL script to ingest, process, and store data.
- `etl/schemas.py`: Python file containing schema definitions for the data.
- `etl/customer_transactions.json`: Sample JSON data for customer transactions.
- `etl/product_catalog.csv`: Sample CSV data for the product catalog.
- `README.md`: This file.

## Prerequisites

- Docker
- Docker Compose

## Setup and Running

1. **Clone the Repository**

    ```sh
    git clone <repository-url>
    cd ShopSmartDataPipeline
    ```

2. **Build and Start the Docker Containers**

    ```sh
    docker-compose up --build
    ```

    This command will build the Docker image for Spark, install necessary dependencies, and start the PostgreSQL and Spark services. The PostgreSQL container will also execute the `init.sql` script to set up the database schema and tables.

3. **Verify Data Ingestion and Processing**

    - The Spark container will automatically run the ETL job defined in `etl/etl_script.py`.
    - The ETL job will read data from `etl/customer_transactions.json` and `etl/product_catalog.csv`, process it, and store the results in the PostgreSQL database.

4. **Access the PostgreSQL Database**

    You can connect to the PostgreSQL database using a database client or the `psql` command-line tool.

    ```sh
    docker exec -it <postgres_container_id> psql -U admin -d shopsmartdb
    ```

    Replace `<postgres_container_id>` with the actual container ID or name of the PostgreSQL container.

## ETL Script Details

The ETL script (`etl/etl_script.py`) performs the following steps:

1. Reads customer transactions data from a JSON file and product catalog data from a CSV file.
2. Cleans and transforms the data, including:
    - Removing rows with NULL values.
    - Removing duplicate rows.
    - Adding `total_amount` column (calculated as `price * quantity`).
    - Adding `created_date` column with the current timestamp.
	- Renaming `timestamp` column with `transaction_date`
3. Joins the transactions data with the product catalog data.
4. Stores the processed data in the PostgreSQL database.

## Schemas

The schemas for the data are defined in `etl/schemas.py`:

- **Customer Transactions Schema**
- **Product Catalog Schema**

## Creating Database Schema and Tables

The SQL script `db_init/init.sql` contains the commands to create the necessary schema and tables.

```sql
-- Create schema and tables

CREATE SCHEMA IF NOT EXISTS sale;

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
```

## Additional Notes

The Dockerfile installs necessary dependencies.
The Spark job will stop automatically after completion.

