from dotenv import load_dotenv
import boto3
import json
load_dotenv()

try:
    print("Attempting Rekognition Connect...")
    rek = boto3.client("rekognition")
    # Empty bytes just to trigger auth check (it will fail with InvalidImageFormat likely, but if Auth fails first we'll see)
    # Actually let's use a dummy image if possible or just list collections
    # But list_collections might verify permissions.
    # checking detect_labels requires an image.
    
    print("Calling list_collections to check generic access...")
    rek.list_collections()
    print("SUCCESS: Rekognition ListCollections worked.")
except Exception as e:
    print("FAILURE: Rekognition failed.")
    print(str(e))
