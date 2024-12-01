import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r'acn-resale-inventories-dde03-firebase-adminsdk-ikyw4-5d72718262.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def upload_json_to_firestore(json_file_path, collection_name):
    # Load JSON data
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Upload each item in JSON to Firestore with kamId as document ID
    for item in data:
        kam_id = item.get("kamId")
        if kam_id:
            try:
                # Set the document ID as kamId
                db.collection(collection_name).document(str(kam_id)).set(item)
                print(f"Successfully uploaded item with kamId {kam_id} to Firestore.")
            except Exception as e:
                print(f"Error uploading item with kamId {kam_id}: {e}")
        else:
            print("Missing kamId, skipping item.")
    
    print(f"Data upload completed for collection '{collection_name}'.")

# Example usage
json_file_path = 'kam.json'  # Replace with your JSON file path
collection_name = 'kam'  # Firestore collection name for kam
upload_json_to_firestore(json_file_path, collection_name)
