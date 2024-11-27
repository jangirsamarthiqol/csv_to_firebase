import csv
import json
import re

def clean_numeric(value):
    """
    Cleans the input value by removing commas and extracting numeric parts.
    Returns a float or int if possible, otherwise returns None.
    """
    if not value or value.strip() in ['--', '']:
        return None
    
    # Remove commas and units if present
    value = re.sub(r'[^\d.,]', '', value).replace(',', '')
    
    # Use regex to extract the first numeric part (integer or float)
    match = re.search(r'(\d+(\.\d+)?)', value)
    if match:
        num_str = match.group(1)
        try:
            return float(num_str) if '.' in num_str else int(num_str)
        except ValueError:
            return None
    return None

def convert_to_boolean(value):
    """
    Converts a string value to a boolean. Treats 'TRUE'/'true' as True and 'FALSE'/'false' as False.
    Returns None for empty or invalid inputs.
    """
    if value.strip().upper() == 'TRUE':
        return True
    elif value.strip().upper() == 'FALSE':
        return False
    return None

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
    
    # Define the fields that should be converted to integers or floats
    numeric_fields = {
        "dailyCredits": "int",
        "monthlyCredits": "int",
        "added": "int",              # Treat 'added' as an integer
        "lastModified": "int"        # Treat 'lastModified' as an integer
    }
    
    # Define the fields that should be converted to booleans
    boolean_fields = ["verified", "blacklisted", "admin"]
    
    # Read the CSV file and process rows
    with open(csv_file_path, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row_num, row in enumerate(csv_reader, start=1):
            # Handle phone number
            phonenumber = row.get("phonenumber", "").strip()
            cleaned_phonenumber = clean_phonenumber(phonenumber)
            if cleaned_phonenumber:
                row["phonenumber"] = cleaned_phonenumber
            else:
                row["phonenumber"] = None
                warnings.append(f"Row {row_num}: Could not clean phone number '{phonenumber}'")
            
            # Handle numeric fields
            for field, dtype in numeric_fields.items():
                original_value = row.get(field, "").strip()
                cleaned_value = clean_numeric(original_value)
                
                if cleaned_value is not None:
                    row[field] = int(cleaned_value) if dtype == "int" else float(cleaned_value)
                else:
                    row[field] = None
                    warnings.append(f"Row {row_num}: Could not convert '{field}' with value '{original_value}' to {dtype}")
            
            # Handle boolean fields
            for field in boolean_fields:
                original_value = row.get(field, "").strip()
                converted_value = convert_to_boolean(original_value)
                
                if converted_value is not None:
                    row[field] = converted_value
                else:
                    row[field] = None
                    warnings.append(f"Row {row_num}: Could not convert '{field}' with value '{original_value}' to boolean")
            
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
csv_file_path = 'agent-db.csv'  # Replace with your CSV file path
json_file_path = r'agent-db.json'  # Replace with desired JSON file path
csv_to_json(csv_file_path, json_file_path)
