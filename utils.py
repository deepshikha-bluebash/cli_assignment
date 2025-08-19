import csv
import hashlib

# Match exactly the column names in your ents.csv
REQUIRED_FIELDS = [
    "Residential Address Street",
    "Residential Address Locality",
    "Residential Address State",
    "Residential Address Postcode"
]

def is_valid_row(row: dict) -> bool:
    """Validate that required address fields are not empty."""
    return all(row.get(field, "").strip() for field in REQUIRED_FIELDS)

def generate_lat_lon(address: str):
    """
    Generate dummy latitude and longitude values based on a hash of the address.
    Ensures values are consistent for the same input.
    """
    h = int(hashlib.md5(address.encode()).hexdigest(), 16)
    latitude = (h % 180) - 90       # range -90 to +90
    longitude = ((h // 180) % 360) - 180  # range -180 to +180
    return latitude, longitude

def process_csv(input_file: str, output_file: str):
    """Read input CSV, validate rows, add latitude & longitude, and write output CSV."""
    with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["latitude", "longitude"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if not is_valid_row(row):
                # skip invalid rows
                continue

            # Build address string from residential address fields
            address = f"{row.get('Residential Address Street','')} {row.get('Residential Address Locality','')} {row.get('Residential Address State','')} {row.get('Residential Address Postcode','')}"
            
            lat, lon = generate_lat_lon(address)
            row["latitude"] = lat
            row["longitude"] = lon
            writer.writerow(row)
