# Use the official Bitnami Spark image as a base
FROM bitnami/spark:latest

# Switch to root user to install wget
USER root

# Ensure the APT package lists directory exists
RUN mkdir -p /var/lib/apt/lists/partial

# Clean up any existing partial lists and update
RUN apt-get clean && apt-get update && apt-get install -y wget

# Download the PostgreSQL JDBC driver directly into the Spark jars directory
RUN wget https://jdbc.postgresql.org/download/postgresql-42.7.3.jar -P /opt/bitnami/spark/jars/

# Switch back to the default user
USER 1001

# Set Spark home and add the PostgreSQL JDBC driver to the classpath
ENV SPARK_HOME=/opt/bitnami/spark
ENV SPARK_CLASSPATH=/opt/bitnami/spark/jars/postgresql-42.7.3.jar

# Copy the ETL script and other necessary files into the container
COPY etl /etl

# Set the working directory
WORKDIR /etl

# Command to run the Spark job
CMD ["/opt/bitnami/spark/bin/spark-submit", "--jars", "/opt/bitnami/spark/jars/postgresql-42.7.3.jar", "/etl/etl_script.py"]

