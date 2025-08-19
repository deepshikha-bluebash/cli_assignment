import sys
from utils import process_csv

def main():
    if len(sys.argv) != 3:
        print("Usage: python assign.py input.csv output.csv")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_csv(input_file, output_file)
    print(f"✅ Processing complete. Output saved to {output_file}")

if __name__ == "__main__":
    main()
