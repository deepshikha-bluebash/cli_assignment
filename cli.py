import argparse
from parser import parse_and_validate_csv

def main():
    parser = argparse.ArgumentParser(description="Client CSV Validator & Enhancer CLI")
    parser.add_argument("input", help="Path to input CSV file")
    parser.add_argument("output", help="Path to output CSV file")
    args = parser.parse_args()

    parse_and_validate_csv(args.input, args.output)

if __name__ == "__main__":
    main()
