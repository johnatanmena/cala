import json
import boto3
import pandas as pd
import io
s3_client = boto3.client("s3")
S3_BUCKET = 'corpstudios'

def lambda_handler(event, context):
  object_key = "stage_area/geografias_panama/nielsen_panama/input_files/ejercicio1_b2.txt" 
  object_key1 = "stage_area/geografias_panama/nielsen_panama/input_files/ejercicio1_b1.xlsx" 
  file_content = s3_client.get_object(Bucket=S3_BUCKET, Key=object_key)["Body"].read()
  file_content1 = s3_client.get_object(Bucket=S3_BUCKET, Key=object_key1)["Body"].read()
  file_content = io.BytesIO(file_content)
  file_content1 = io.BytesIO(file_content1)
  print(file_content)
  return [file_content,file_content1]