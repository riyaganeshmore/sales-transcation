<!DOCTYPE html>
<html lang="en">
<body>

  <h1>🧾 Sales Transactions Aggregator Using AWS Glue & S3</h1>

  <h2>📌 Overview</h2>
  <p>This project demonstrates a serverless ETL pipeline using <strong>AWS Glue</strong> and <strong>Amazon S3</strong>. It processes <strong>daily sales transaction data</strong> from multiple stores, enriches it with metadata, filters out invalid records, and generates <strong>aggregated sales reports</strong>.</p>

  <h2>🧱 Architecture Components</h2>
  <table>
    <tr><th>Service</th><th>Purpose</th></tr>
    <tr><td>Amazon S3</td><td>Storage for raw input files, metadata, and processed output</td></tr>
    <tr><td>AWS Glue</td><td>Serverless ETL job to transform and process data</td></tr>
    <tr><td>Glue Data Catalog</td><td>Manages metadata for sales and store tables</td></tr>
    <tr><td>Amazon Athena (optional)</td><td>SQL-based querying of processed output</td></tr>
  </table>

  <h2>📂 Input Data</h2>

  <h3>🛒 1. Daily Sales Transactions</h3>
  <p><strong>Location:</strong> <code>s3://salesinfo-bucket1/raw/daily-sales/</code></p>
  <p><strong>Format:</strong> JSON or CSV</p>
  <pre>{
  "transaction_id": "TXN00123",
  "store_id": "S101",
  "product_id": "P202",
  "sales_amount": 450.00,
  "timestamp": "2025-06-10T14:35:00Z"
}</pre>

  <h3>🏬 2. Store Metadata</h3>
  <p><strong>Location:</strong> <code>s3://salesinfo-bucket1/reference/store_metadata.csv</code></p>
  <p><strong>Format:</strong> CSV</p>
  <pre>store_id,store_name,location,manager_name
S101,ABC Store,Mumbai,John Doe
S102,XYZ Store,Pune,Jane Smith</pre>

  <h2>🔄 ETL Workflow (AWS Glue)</h2>

  <ol>
    <li><strong>Load Data:</strong> Read daily sales and store metadata from S3.</li>
    <li><strong>Join:</strong> Enrich sales data with store metadata using <code>store_id</code>.</li>
    <li><strong>Clean:</strong> Remove transactions with missing or invalid fields (e.g., null or ≤ 0 sales).</li>
    <li><strong>Aggregate:</strong> Group by <code>store_id</code> and <code>product_id</code>, summing total sales.</li>
    <li><strong>Write Output:</strong> Save cleaned and aggregated data back to S3 in Parquet format.</li>
  </ol>

  <h2>🧪 Sample Glue Script (PySpark)</h2>
  <pre>
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

# Join datasets
joined_df = sales_df.join(metadata_df, on="store_id", how="inner")

# Filter invalid data
valid_df = joined_df.filter(
    (col("sales_amount").isNotNull()) & 
    (col("sales_amount") > 0)
)

# Aggregate sales
agg_df = valid_df.groupBy("store_id", "product_id") \
                 .agg(sum("sales_amount").alias("total_sales"))

# Write to S3
agg_df.write.mode("overwrite").parquet("s3://salesinfo-bucket1/processed/aggregated-sales/")
  </pre>

  <h2>✅ Output Example</h2>
  <table>
    <tr><th>store_id</th><th>product_id</th><th>total_sales</th></tr>
    <tr><td>S101</td><td>P202</td><td>14,500.00</td></tr>
    <tr><td>S102</td><td>P201</td><td>9,800.00</td></tr>
  </table>
  <p><strong>Output Location:</strong> <code>s3://salesinfo-bucket1/processed/aggregated-sales/</code></p>

  <h2>🚧 Error Handling</h2>
  <div class="highlight">
    If you see the following error when accessing the file:
    <pre>
&lt;Error&gt;
  &lt;Code&gt;AccessDenied&lt;/Code&gt;
  &lt;Message&gt;Access Denied&lt;/Message&gt;
&lt;/Error&gt;
    </pre>
    <strong>Solution:</strong>
    <ul>
      <li>Ensure the IAM Role used by Glue has correct S3 read/write permissions</li>
      <li>Make the S3 object or bucket publicly accessible (if required)</li>
      <li>Check for missing pre-signed URL or wrong region</li>
    </ul>
  </div>

  <h2>📈 Optional: Query With Amazon Athena</h2>
  <pre>
SELECT store_id, product_id, total_sales
FROM "salesinfo"."aggregated_sales"
ORDER BY total_sales DESC;
  </pre>

  <h2>📌 Technologies Used</h2>
  <ul>
    <li>AWS Glue</li>
    <li>Amazon S3</li>
    <li>PySpark</li>
    <li>AWS IAM</li>
    <li>Optional: Amazon Athena</li>
  </ul>

  <h2>👥 Team Members</h2>
  <ul>
    <li>Your Name</li>
    <li>Teammate 2</li>
    <li>Teammate 3</li>
  </ul>

  <h2>📁 Repository Structure</h2>
  <pre>
├── glue-scripts/
│   └── etl_sales_transform.py
├── sample-data/
│   ├── daily_sales_sample.json
│   └── store_metadata.csv
├── README.html
└── architecture-diagram.png
  </pre>

</body>
</html>
