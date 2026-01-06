from dotenv import load_dotenv
import boto3
load_dotenv()

def check_service(name, client_name, func):
    try:
        client = boto3.client(client_name)
        func(client)
        print(f"[OK] {name}")
    except Exception as e:
        print(f"[FAIL] {name}: {e}")

print("Checking permissions...")

# Check S3
check_service("S3 (List Buckets)", "s3", lambda c: c.list_buckets())

# Check Bedrock (List Foundation Models)
check_service("Bedrock (List Models)", "bedrock", lambda c: c.list_foundation_models())

# Check Polly (Describe Voices)
check_service("Polly (Describe Voices)", "polly", lambda c: c.describe_voices())
