import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"

def check_bedrock(region):
    print(f"Checking Bedrock in {region}...")
    try:
        # Force region for this client
        runtime = boto3.client("bedrock-runtime", region_name=region)
        runtime.invoke_model(
            modelId=MODEL_ID, 
            body='{"anthropic_version":"bedrock-2023-05-31","max_tokens":1,"messages":[{"role":"user","content":"Hi"}]}'
        )
        print(f"SUCCESS: Bedrock works in {region}")
        return True
    except Exception as e:
        print(f"FAILURE in {region}: {e}")
        return False

# Check both likely regions
r1 = check_bedrock("us-east-1")
r2 = check_bedrock("us-east-2")
