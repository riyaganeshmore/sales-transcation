import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame
import re

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Amazon S3
AmazonS3_node1749627973586 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://iol-sales-info/raw data/Sales Transactions raw.csv"], "recurse": True}, transformation_ctx="AmazonS3_node1749627973586")

# Script generated for node Filter
Filter_node1749628016120 = Filter.apply(frame=AmazonS3_node1749627973586, f=lambda row: (bool(re.match("0", row["quantity"]))), transformation_ctx="Filter_node1749628016120")

# Script generated for node SQL Query
SqlQuery56 = '''
Total_Sales = Quantity * Unit_Price

'''
SQLQuery_node1749628057376 = sparkSqlQuery(glueContext, query = SqlQuery56, mapping = {"myDataSource":Filter_node1749628016120}, transformation_ctx = "SQLQuery_node1749628057376")

job.commit()