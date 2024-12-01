import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r'acn-resale-inventories-dde03-firebase-adminsdk-ikyw4-5d72718262.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def upload_json_to_firestore(json_file_path, collection_name):
    """
    Uploads JSON data to Firestore, using 'cpId' as the document ID.
    Supports batch writing for better performance and logs warnings for issues.
    """
    # Load JSON data
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    batch = db.batch()  # Initialize Firestore batch
    batch_size = 500  # Firestore batch limit
    current_batch_count = 0

    warnings = []  # Collect warnings for missing fields or errors
    total_uploaded = 0

    for item in data:
        try:
            # Ensure mandatory fields exist
            cp_id = item.get('cpId')
            phone_number = item.get('phonenumber')
            
            if not cp_id:
                warnings.append(f"Skipping item without 'cpId': {item}")
                continue

            if not phone_number:
                warnings.append(f"Skipping item without 'phonenumber': {item}")
                continue

            # Prepare document reference
            document_id = str(cp_id)
            doc_ref = db.collection(collection_name).document(document_id)

            # Add item to batch
            batch.set(doc_ref, item)
            current_batch_count += 1
            total_uploaded += 1

            # Commit the batch when the batch size limit is reached
            if current_batch_count >= batch_size:
                batch.commit()
                print(f"Uploaded {current_batch_count} items in a batch.")
                batch = db.batch()  # Start a new batch
                current_batch_count = 0

        except Exception as e:
            warnings.append(f"Error uploading item {item}: {e}")

    # Commit the remaining items in the batch
    if current_batch_count > 0:
        batch.commit()
        print(f"Uploaded {current_batch_count} remaining items in the final batch.")

    # Log warnings if any
    if warnings:
        log_file_path = "firestore_upload_warnings.log"
        with open(log_file_path, "w", encoding="utf-8") as log_file:
            for warning in warnings:
                log_file.write(warning + "\n")
        print(f"Warnings logged in '{log_file_path}'.")

    # Final summary
    print(f"Data uploaded successfully to Firestore collection '{collection_name}'.")
    print(f"Total items uploaded: {total_uploaded}")
    if warnings:
        print(f"Total warnings: {len(warnings)} (See '{log_file_path}' for details).")

# Example usage
json_file_path = 'agent-db.json'  # Replace with your JSON file path
collection_name = 'agents'  # Firestore collection name for agents
upload_json_to_firestore(json_file_path, collection_name)
