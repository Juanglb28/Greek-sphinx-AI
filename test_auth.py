from dotenv import load_dotenv
import boto3
import json
load_dotenv()

try:
    sts = boto3.client("sts")
    identity = sts.get_caller_identity()
    print("SUCCESS: Credentials are valid.")
    print(f"Account: {identity['Account']}")
    print(f"ARN: {identity['Arn']}")
except Exception as e:
    print("FAILURE: Credentials rejected.")
    print(str(e))
