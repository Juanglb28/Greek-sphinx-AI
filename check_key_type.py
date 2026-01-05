from dotenv import load_dotenv
import os
load_dotenv()

key = os.getenv("AWS_ACCESS_KEY_ID", "")
print(f"Key starts with AKIA: {key.startswith('AKIA')}")
print(f"Key starts with ASIA: {key.startswith('ASIA')}")
