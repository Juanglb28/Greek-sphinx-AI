from dotenv import load_dotenv
import boto3
import os
load_dotenv()

bucket = os.getenv("S3_BUCKET")
print(f"Checking location for: {bucket}")
s3 = boto3.client("s3")
try:
    loc = s3.get_bucket_location(Bucket=bucket)
    print(f"Location Constraint: {loc['LocationConstraint']}")
except Exception as e:
    print(f"Error: {e}")
