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
    
    # Remove commas
    value = value.replace(',', '')
    
    # Use regex to extract the first numeric part (integer or float)
    match = re.search(r'(\d+(\.\d+)?)', value)
    if match:
        num_str = match.group(1)
        if '.' in num_str:
            try:
                return float(num_str)
            except ValueError:
                return None
        else:
            try:
                return int(num_str)
            except ValueError:
                return None
    return None

def csv_to_json(csv_file_path, json_file_path):
    data = []
    
    # Define the fields that should be converted to integers or floats
    # The value is the desired type: 'int' or 'float'
    numeric_fields = {
        "plotSize": "float",       # Assuming plotSize can be fractional or have units
        "carpet": "int",
        "sbua": "int",
        "totalAskPrice": "float",
        "askPricePerSqft": "float",
        "geOfInventory": "int",
        "ageOfStatus": "int"
    }
    
    # Read the CSV file and add each row to the data list
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row_num, row in enumerate(csv_reader, start=1):
            for field, dtype in numeric_fields.items():
                original_value = row.get(field, "").strip()
                cleaned_value = clean_numeric(original_value)
                
                if cleaned_value is not None:
                    if dtype == "int":
                        row[field] = int(cleaned_value)
                    elif dtype == "float":
                        row[field] = float(cleaned_value)
                else:
                    # Optionally, set to None or a default value
                    row[field] = None
                    print(f"Warning: Could not convert field '{field}' with value '{original_value}' to {dtype} (Row {row_num})")
            data.append(row)
    
    # Write the data list to a JSON file
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"CSV data has been successfully converted to JSON and saved to {json_file_path}")

# Example usage
csv_file_path = 'acn.csv'  # Replace with your CSV file path
json_file_path = r'D:\Development\csv-to-json\output.json'  # Replace with desired JSON file path
csv_to_json(csv_file_path, json_file_path)
