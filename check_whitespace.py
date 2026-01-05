from dotenv import load_dotenv
import os
load_dotenv()

key = os.getenv("AWS_ACCESS_KEY_ID", "")
secret = os.getenv("AWS_SECRET_ACCESS_KEY", "")

def check_whitespace(name, value):
    if not value: return
    if value.strip() != value:
        print(f"WARNING: {name} has leading/trailing whitespace!")
        print(f"'{name}' -> '{value}'")
    else:
        print(f"{name} looks clean.")

check_whitespace("AWS_ACCESS_KEY_ID", key)
check_whitespace("AWS_SECRET_ACCESS_KEY", secret)
