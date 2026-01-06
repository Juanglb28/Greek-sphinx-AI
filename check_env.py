from dotenv import load_dotenv
import os
load_dotenv()

cors = os.getenv("CORS_ORIGINS")
aws_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")

print(f"CORS_ORIGINS: {cors}")
print(f"AWS_ACCESS_KEY_ID Set: {bool(aws_key)}")
if aws_key:
    print(f"AWS_ACCESS_KEY_ID Length: {len(aws_key)}")
print(f"AWS_SECRET_ACCESS_KEY Set: {bool(aws_secret)}")
