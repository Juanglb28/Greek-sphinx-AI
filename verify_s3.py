from dotenv import load_dotenv
import boto3
import os
from botocore.exceptions import ClientError

load_dotenv()

bucket_name = os.getenv("S3_BUCKET")
print(f"Checking bucket: {bucket_name}")

s3 = boto3.client("s3")

try:
    s3.head_bucket(Bucket=bucket_name)
    print("SUCCESS: Bucket exists and is accessible.")
    
    # Check ACL settings implicitly by checking if we can get policy status or just warn user
    # Ideally we try a small put with ACL public-read if we want to be 100% sure about the error we saw earlier
except ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == '404':
        print("FAILURE: Bucket does not exist (404).")
    elif error_code == '403':
        print("FAILURE: Access Denied (403). Check permissions.")
    else:
        print(f"FAILURE: {e}")
