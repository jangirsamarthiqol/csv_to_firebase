import csv
import json
import re

def clean_phonenumber(value):
    """
    Cleans the phone number by removing non-numeric characters and adding +91 as prefix.
    Returns a cleaned phone number as a string.
    """
    if not value or value.strip() in ['--', '']:
        return None
    
    # Remove non-numeric characters
    cleaned_value = re.sub(r'\D', '', value)
    
    # Ensure the cleaned value has exactly 10 digits, then prefix with +91
    if len(cleaned_value) == 10:
        return f"+91{cleaned_value}"
    
    # Return None if phone number is not valid
    return None

def csv_to_json(csv_file_path, json_file_path):
    data = []
    warnings = []
    
    # Read the CSV file and process rows
    with open(csv_file_path, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row_num, row in enumerate(csv_reader, start=1):
            # Clean phone number
            phonenumber = row.get("phoneNumber", "").strip()
            cleaned_phonenumber = clean_phonenumber(phonenumber)
            if cleaned_phonenumber:
                row["phoneNumber"] = cleaned_phonenumber
            else:
                row["phoneNumber"] = None
                warnings.append(f"Row {row_num}: Could not clean phone number '{phonenumber}'")
            
            # Handle 'myAgents' field, clean it and make it an array
            my_agents = row.get("myAgents", "").strip()
            if my_agents:
                # Remove extra quotes and split by comma
                row["myAgents"] = [agent.strip().replace('"', '') for agent in my_agents.split(',')]
            else:
                row["myAgents"] = []
            
            # Treat all other fields as strings
            for field in ["kamId", "name", "email", "linkedin", "profilePic"]:
                row[field] = row.get(field, "").strip()
            
            data.append(row)
    
    # Write to JSON
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)
    
    # Write warnings to log file
    with open("conversion_warnings.log", "w", encoding="utf-8") as log_file:
        for warning in warnings:
            log_file.write(warning + "\n")
    
    print(f"CSV data successfully converted to JSON at {json_file_path}")
    print(f"Conversion warnings logged in 'conversion_warnings.log'")

# Example usage
csv_file_path = 'kam.csv'  # Replace with your CSV file path
json_file_path = r'kam.json'  # Replace with desired JSON file path
csv_to_json(csv_file_path, json_file_path)
