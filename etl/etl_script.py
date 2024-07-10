import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, from_utc_timestamp
from schemas import transactions_schema, products_schema  # Import schemas

# Initialize Spark Session
spark = SparkSession.builder\
    .appName("ShopSmart") \
    .config("spark.jars", "/opt/bitnami/spark/jars/postgresql-42.7.3.jar") \
    .getOrCreate()\

#Ingest Customer Transactions from JSON file and Product Catalog from CSV file
transactions_df = spark.read.schema(transactions_schema).json("customer_transactions.json", multiLine=True)
products_df = spark.read.schema(products_schema).csv("product_catalog.csv", header=True, inferSchema=True)

#Cleaning data -- Drop null and Duplicate then filter all invalid value
cleaned_products_df = products_df.dropna().filter(products_df['price'] >= 0).dropDuplicates()
cleaned_transactions_df = transactions_df.dropna().dropDuplicates()

#Transform Data -- Add column total_amount, created_date and Rename column timestamp 
cleaned_transactions_df = cleaned_transactions_df.withColumn("total_amount", col("price") * col("quantity")).withColumn("created_date", from_utc_timestamp(current_timestamp(), "GMT+7")).withColumnRenamed("timestamp","transaction_date")

#Join Data
unified_df = cleaned_transactions_df.join(cleaned_products_df, on="product_id")

selected_columns_df = unified_df.select(
    cleaned_transactions_df["transaction_id"],
    cleaned_transactions_df["customer_id"],
    cleaned_transactions_df["product_id"],
    cleaned_products_df["product_name"],
    cleaned_products_df["category"],
    cleaned_transactions_df["quantity"],
    cleaned_transactions_df["price"],
    cleaned_transactions_df["total_amount"],
    cleaned_transactions_df["transaction_date"],
    cleaned_transactions_df["created_date"]
)

# Load Data into PostgreSQL
selected_columns_df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres:5432/shopsmartdb") \
    .option("dbtable", "sale.transactions") \
    .option("user", "admin") \
    .option("password", "0000") \
    .option("driver", "org.postgresql.Driver") \
    .mode("append")\
    .save()

spark.stop()