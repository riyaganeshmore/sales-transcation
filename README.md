<h1>🧾 Sales Transactions Aggregator Using AWS Glue & S3</h1><br>
<h2>📌 Overview</h2><br>
This project demonstrates a serverless ETL pipeline using AWS Glue and Amazon S3. It processes daily sales transaction data from multiple stores, enriches it with metadata, filters out invalid records, and generates aggregated sales reports.<br><br>

This solution is useful for retail or e-commerce businesses looking to build automated reporting systems based on cloud-native architecture.<br>

<h2>🧱 Architecture Components</h2><br>
Service	<br>
Amazon S3	Storage for raw input files, metadata, and processed output<br>
AWS Glue	Serverless ETL job to transform and process data<br>
Glue Data Catalog	Manages metadata for sales and store tables<br>
Amazon Athena (optional)	SQL-based querying of processed output<br>

<h2>📂 Input Data</h2><br>
🛒 1. Daily Sales Transactions<br>
Location: s3://salesinfo-bucket1/raw/daily-sales/<br>

Format: JSON or CSV<br>

Example:<br>

json<br>
Copy<br>
Edit<br>
{
  "transaction_id": "TXN00123",<br>
  "store_id": "S101",<br>
  "product_id": "P202",<br>
  "sales_amount": 450.00,<br>
  "timestamp": "2025-06-10T14:35:00Z"<br>
}<br><br>
<h2>🏬 2. Store Metadata</h2><br>
Location: s3://salesinfo-bucket1/reference/store_metadata.csv<br>

Format: CSV<br>

Example:<br>
<br>
cs<br>
Copy<br>
Edit<br>
store_id,store_name,location,manager_name<br>
S101,ABC Store,Mumbai,John Doe<br>
S102,XYZ Store,Pune,Jane Smith<br><br>
<h2>🔄 ETL Workflow (AWS Glue)</h2><br><br>
<Step 1: Load Data<br>
Read daily sales transactions and store metadata from Amazon S3.<br><br>

<Step 2: Join Datasets<br>
Perform an inner join on store_id to enrich sales data with store details like location and manager name.<br>
<br><br>
<Step 3: Clean Data<br>
Filter out records with:<br>

Null or missing store_id, product_id, or sales_amount<br>

sales_amount ≤ 0<br>

Step 4: Aggregate Sales<br><br>
Group by store_id and product_id<br>

Calculate total sales using Spark aggregation<br><br>

<Step 5: Write Output<br>
Store final aggregated output in s3://salesinfo-bucket1/processed/aggregated-sales/<br>

Format: Parquet (for optimized storage and query performance)<br>

<h2>👥 Team Members</h2><br>
Team 9<br>
Riya More<br>
Bhumika Wadhwani<br>
Suraj Sharma<br>
Rakhi Sathi<br>
Amardeep Patel<br>
Anil <br>

<h2>📁 Repository Structure</h2>br>
bash<br>
Copy<br>
Edit<br>
├── glue-scripts/<br>
│   └── etl_sales_transform.py <br>     
├── sample-data/<br>
│   ├── daily_sales_sample.json<br>
│   └── store_metadata.csv<br>
├── README.md<br>                     
└── architecture-diagram.png<br>         


Format: Parquet or CSV for optimized storage and analytics

Optional: Partition the data by store_id or date for better querying
