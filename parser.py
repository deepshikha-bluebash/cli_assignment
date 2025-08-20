import csv
from geo import get_coordinates

def is_valid_row(row):
    """Check if all required fields are present and non-empty."""
    required_fields = [
        row.get('Email'), row.get('First Name'), row.get('Last Name'),
        row.get('Residential Address Street'), row.get('Residential Address Locality'),
        row.get('Residential Address State'), row.get('Residential Address Postcode'),
        row.get('Postal Address Street'), row.get('Postal Address Locality'),
        row.get('Postal Address State'), row.get('Postal Address Postcode')
    ]
    return all(required_fields)

def clean_postcode(value):
    """Convert postcode to string without decimals."""
    try:
        return str(int(float(value)))
    except (ValueError, TypeError):
        return ''

def parse_and_validate_csv(input_path, output_path):
    """Parse, validate, enhance CSV with Latitude & Longitude."""
    with open(input_path, 'r', newline='', encoding='utf-8') as infile, \
         open(output_path, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Latitude', 'Longitude']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        count = 0
        for row in reader:
            if not is_valid_row(row):
                print("Invalid row (missing required fields):", row)
                continue

            postcode = clean_postcode(row['Residential Address Postcode'])
            address = f"{row['Residential Address Locality']}, {row['Residential Address State']} {postcode}, Australia"
            print("Looking up address:", address)

            try:
                coords = get_coordinates(address)
            except Exception as e:
                print("Unexpected error:", e)
                coords = None

            row['Latitude'], row['Longitude'] = coords if coords else (None, None)
            writer.writerow(row)
            count += 1
            print(f"Processed {count} valid rows...")
