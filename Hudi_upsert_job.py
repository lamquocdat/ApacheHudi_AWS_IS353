import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, to_timestamp, monotonically_increasing_id, to_date, when, lit
import json

args = getResolvedOptions(
    sys.argv, ['JOB_NAME',
               'SOURCE_S3_PATH',
               'GLUE_DATABASE', 'GLUE_TABLE_NAME', 'HUDI_PRECOMB_KEY', 'HUDI_RECORD_KEY', 'UPDATES',
               'TARGET_S3_PATH']
)

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

S3bucket_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": [args['SOURCE_S3_PATH']],
        "recurse": True,
    },
    transformation_ctx="S3bucket_node1",
)

# Script generated for node S3 bucket
additional_options = {
    "hoodie.table.name": args['GLUE_TABLE_NAME'],
    "hoodie.datasource.write.table.type": "MERGE_ON_READ",
    "hoodie.datasource.write.operation": "upsert",
    "hoodie.datasource.write.recordkey.field": args['HUDI_RECORD_KEY'],
    "hoodie.datasource.write.precombine.field": args['HUDI_PRECOMB_KEY'],
    "hoodie.datasource.write.hive_style_partitioning": "true",
    "hoodie.parquet.compression.codec": "gzip",
    "hoodie.datasource.hive_sync.enable": "true",
    "hoodie.datasource.hive_sync.database": args['GLUE_DATABASE'],
    "hoodie.datasource.hive_sync.table": args['GLUE_TABLE_NAME'],
    "hoodie.datasource.hive_sync.partition_extractor_class": "org.apache.hudi.hive.MultiPartKeysValueExtractor",
    "hoodie.datasource.hive_sync.use_jdbc": "false",
    "hoodie.datasource.hive_sync.mode": "hms",
}
S3bucket_node3_df = S3bucket_node1.toDF()

if(args['UPDATES']):
    for value in json.loads(args['UPDATES']):
        S3bucket_node3_df = S3bucket_node3_df.withColumn(value[0], when(S3bucket_node3_df[value[0]] == value[1], lit(value[2]))\
        .otherwise(S3bucket_node3_df[value[0]]))
    
try:
    S3bucket_node3_df.write.format("hudi").options(**additional_options).mode(
        "append"
    ).save(args['TARGET_S3_PATH'])
except Exception as e:
    print("Error : {} ".format(e))


job.commit()