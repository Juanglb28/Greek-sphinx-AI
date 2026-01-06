from dotenv import load_dotenv
import boto3
import json
load_dotenv()

def test_perm(name, func):
    try:
        func()
        print(f"[OK] {name}")
    except Exception as e:
        print(f"[FAIL] {name}: {e}")

print("Verifying Policy Permissions...")

# 1. S3 PutObject (Check if we can list or just try a dummy put if possible, but Put is hard to test without writing. 
# We'll trust Put works if we have it, but let's try ListBuckets which is NOT in the policy to confirm strictness, 
# or just assume user applied what they shared.)
# The policy DOES NOT have ListBuckets. So client.list_buckets() should FAIL.
# The policy HAS PutObject.

s3 = boto3.client("s3")
test_perm("S3 ListBuckets (Should Fail)", lambda: s3.list_buckets())

# 2. Rekognition DetectLabels
rek = boto3.client("rekognition")
# We need an image to test detect_labels, or at least pass empty bytes to trigger validation error (not auth error)
test_perm("Rekognition DetectLabels", lambda: rek.detect_labels(Image={'Bytes': b'000'}, MaxLabels=1))

# 3. Bedrock InvokeModel
bed = boto3.client("bedrock-runtime")
# We can't really test invoke without a valid model and payload, it might cost money or error.
# But list_foundation_models is NOT in policy.
test_perm("Bedrock ListFoundationModels (Should Fail)", lambda: boto3.client("bedrock").list_foundation_models())

# 4. Polly SynthesizeSpeech
pol = boto3.client("polly")
test_perm("Polly SynthesizeSpeech", lambda: pol.synthesize_speech(Text="Test", OutputFormat="mp3", VoiceId="Joanna"))
