🧾 Sales Transactions Aggregator Using AWS Glue & S3
📌 Overview
This project demonstrates a serverless ETL pipeline using AWS Glue and Amazon S3. It processes daily sales transaction data from multiple stores, enriches it with metadata, filters out invalid records, and generates aggregated sales reports.

This solution is useful for retail or e-commerce businesses looking to build automated reporting systems based on cloud-native architecture.

🧱 Architecture Components
Service	Purpose
Amazon S3	Storage for raw input files, metadata, and processed output
AWS Glue	Serverless ETL job to transform and process data
Glue Data Catalog	Manages metadata for sales and store tables
Amazon Athena (optional)	SQL-based querying of processed output

📂 Input Data
🛒 1. Daily Sales Transactions
Location: s3://salesinfo-bucket1/raw/daily-sales/

Format: JSON or CSV

Example:

json
Copy
Edit
{
  "transaction_id": "TXN00123",
  "store_id": "S101",
  "product_id": "P202",
  "sales_amount": 450.00,
  "timestamp": "2025-06-10T14:35:00Z"
}
🏬 2. Store Metadata
Location: s3://salesinfo-bucket1/reference/store_metadata.csv

Format: CSV

Example:

cs
Copy
Edit
store_id,store_name,location,manager_name
S101,ABC Store,Mumbai,John Doe
S102,XYZ Store,Pune,Jane Smith
🔄 ETL Workflow (AWS Glue)
Step 1: Load Data
Read daily sales transactions and store metadata from Amazon S3.

Step 2: Join Datasets
Perform an inner join on store_id to enrich sales data with store details like location and manager name.

Step 3: Clean Data
Filter out records with:

Null or missing store_id, product_id, or sales_amount

sales_amount ≤ 0

Step 4: Aggregate Sales
Group by store_id and product_id

Calculate total sales using Spark aggregation

Step 5: Write Output
Store final aggregated output in s3://salesinfo-bucket1/processed/aggregated-sales/

Format: Parquet (for optimized storage and query performance)

🧪 Sample Glue Script (PySpark)
python
Copy
Edit
from pyspark.sql.functions import col, sum
from awsglue.context import GlueContext
from pyspark.context import SparkContext

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Load sales data
sales_df = spark.read.json("s3://salesinfo-bucket1/raw/daily-sales/")

# Load store metadata
metadata_df = spark.read.csv("s3://salesinfo-bucket1/reference/store_metadata.csv", header=True)

# Join sales with store metadata
joined_df = sales_df.join(metadata_df, on="store_id", how="inner")

# Filter invalid transactions
valid_df = joined_df.filter(
    (col("sales_amount").isNotNull()) & 
    (col("sales_amount") > 0)
)

# Aggregate total sales per store and product
agg_df = valid_df.groupBy("store_id", "product_id") \
                 .agg(sum("sales_amount").alias("total_sales"))

# Write the output to S3 in Parquet format
agg_df.write.mode("overwrite").parquet("s3://salesinfo-bucket1/processed/aggregated-sales/")
✅ Output Example
store_id	product_id	total_sales
S101	P202	14,500.00
S102	P201	9,800.00

Stored in S3 at: s3://salesinfo-bucket1/processed/aggregated-sales/

Format: Parquet (optionally CSV)

🚧 Error Handling
If you see an error like:

xml
Copy
Edit
<Error>
  <Code>AccessDenied</Code>
  <Message>Access Denied</Message>
</Error>
Possible Solutions:
Ensure S3 object/bucket is publicly accessible (if intended)

Use a pre-signed URL for restricted access

Check IAM roles and policies for the Glue job

Verify S3 bucket permissions allow s3:GetObject and s3:PutObject

📈 Optional: Query Using Amazon Athena
After the ETL is complete, you can query the output data in Athena using SQL:

sql
Copy
Edit
SELECT store_id, product_id, total_sales
FROM "salesinfo"."aggregated_sales"
ORDER BY total_sales DESC;
📌 Technologies Used
AWS Glue

Amazon S3

PySpark (Spark DataFrame API)

AWS IAM

Optionally: Amazon Athena

👥 Team Members
[Your Name]

[Team Member 2]

[Team Member 3]

📁 Repository Structure
bash
Copy
Edit
├── glue-scripts/
│   └── etl_sales_transform.py       # Glue ETL job script
├── sample-data/
│   ├── daily_sales_sample.json
│   └── store_metadata.csv
├── README.md                        # Project documentation
└── architecture-diagram.png         # Optional: Visual of the data pipeline


Format: Parquet or CSV for optimized storage and analytics

Optional: Partition the data by store_id or date for better querying
