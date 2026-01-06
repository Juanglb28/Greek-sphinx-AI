from dotenv import load_dotenv
import os
load_dotenv()

region = os.getenv("AWS_REGION")
secret = os.getenv("AWS_SECRET_ACCESS_KEY")
token = os.getenv("AWS_SESSION_TOKEN")

print(f"AWS_REGION: {region}")
if secret:
    print(f"AWS_SECRET_ACCESS_KEY Length: {len(secret)}")
else:
    print("AWS_SECRET_ACCESS_KEY: Not Set")

if token:
    print(f"AWS_SESSION_TOKEN Set: Yes (Length: {len(token)})")
else:
    print("AWS_SESSION_TOKEN: Not Set")
