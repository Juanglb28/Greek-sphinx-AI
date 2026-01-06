import boto3
import json
from botocore.exceptions import ClientError
from dotenv import load_dotenv
load_dotenv()

MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"

print(f"Checking access for model: {MODEL_ID}")

try:
    bedrock = boto3.client("bedrock")
    # List foundation models to see if it's listed and what the status looks like (though strictly list doesn't show subscription)
    # The best check is to try to invoke it.
    
    runtime = boto3.client("bedrock-runtime")
    
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 10,
        "messages": [{"role": "user", "content": "Hi"}]
    }

    print("Attempting to invoke model...")
    response = runtime.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(payload)
    )
    print("SUCCESS: Model is accessible!")
    
except ClientError as e:
    print(f"FAILURE: {e}")
    if "AccessDeniedException" in str(e):
        print("\nPOSSIBLE CAUSE: You might need to 'Request Model Access' in the AWS Bedrock Console.")
        print("Go to AWS Console > Bedrock > Model access > Manage model access > Check 'Claude 3 Haiku' > Save changes.")
except Exception as e:
    print(f"ERROR: {e}")
