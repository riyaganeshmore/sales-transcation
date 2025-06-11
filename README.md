<h2>Project Title: Sales Transactions Aggregator using AWS Glue and S3</h2><br>
🔍 Objective<br>
To design and implement a data processing pipeline that collects daily sales data from multiple stores, processes it using AWS Glue, and generates aggregated sales reports per store and product. This enables business teams to gain insights into store performance, popular products, and overall sales trends.<br>

🧱 Architecture Components
Component	Description
Amazon S3	Used as the storage layer for raw input files, reference metadata, and processed output
AWS Glue	Serverless ETL tool used to transform and join datasets using PySpark
Glue Data Catalog	Stores metadata definitions (tables) for input/output data
Amazon Athena (optional)	Can be used to query processed data interactively<br>

📂 Input Data
1. Daily Sales Transactions
Location: s3://salesinfo-bucket1/raw/daily-sales/

Format: JSON or CSV

Schema Example:

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
2. Store Metadata
Location: s3://salesinfo-bucket1/reference/store_metadata.csv

Format: CSV

Schema Example:

csv
Copy
Edit
store_id,store_name,location,manager_name
S101,ABC Store,Mumbai,John Doe
S102,XYZ Store,Pune,Jane Smith<br><br>
🔄 Data Processing Steps Using AWS Glue<br>
Step 1: Data Ingestion
AWS Glue reads both:

Daily sales transaction data from the raw sales S3 bucket

Store metadata from the reference S3 location
<br>
Step 2: Data Joining
A join operation is performed between sales data and store metadata on store_id to enrich the sales data with store details such as location and manager.
<br>
Step 3: Data Cleaning
Filter out invalid transactions:

Missing or null values in store_id, product_id, or sales_amount

sales_amount less than or equal to 0
<br>
Step 4: Aggregation
Group data by store_id and product_id

Calculate the total sales using aggregation functions
<br>
Step 5: Output
Store the final, processed data back into S3:

Location: s3://salesinfo-bucket1/processed/aggregated-sales/

Format: Parquet or CSV for optimized storage and analytics

Optional: Partition the data by store_id or date for better querying
