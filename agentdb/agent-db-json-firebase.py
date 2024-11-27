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

    # Upload each item in JSON to Firestore with random document ID
    for item in data:
        try:
            db.collection(collection_name).add(item)
        except Exception as e:
            print(f"Error uploading item {item}: {e}")

    print(f"Data uploaded successfully to Firestore collection '{collection_name}' with random document IDs.")

# Example usage
json_file_path = 'agent-db.json'  # Replace with your JSON file path
collection_name = 'agents'  # Firestore collection name for agents
upload_json_to_firestore(json_file_path, collection_name)
