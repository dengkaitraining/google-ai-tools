import os
import re
import subprocess

def main():
    tickets_dir = "Tickets"
    if not os.path.exists(tickets_dir):
        print(f"Error: Directory '{tickets_dir}' does not exist.")
        return

    # Find all PDF files matching the pattern [YYYYMMDD-HHMM][Price]OriginalName.pdf
    pattern = re.compile(r"^\[(\d{8}-\d{4})\]\[(\d+)\].*\.pdf$")
    matching_files = []
    total_fare = 0

    for filename in os.listdir(tickets_dir):
        match = pattern.match(filename)
        if match:
            # Store tuple of (time_str, filename, price) for sorting and summation
            price = int(match.group(2))
            matching_files.append((match.group(1), filename, price))

    if not matching_files:
        print("No renamed PDF files found to merge.")
        return

    # Sort chronologically by the time prefix
    matching_files.sort()
    
    # Get the sorted list of file paths and calculate total fare
    input_paths = []
    for _, filename, price in matching_files:
        input_paths.append(os.path.join(tickets_dir, filename))
        total_fare += price
    
    output_path = os.path.join(tickets_dir, "merged_tickets.pdf")

    print(f"Found {len(input_paths)} files to merge:")
    for _, filename, price in matching_files:
        print(f"  - {os.path.join(tickets_dir, filename)} (Fare: NT$ {price})")

    print(f"\nTotal Fare (費用加總): NT$ {total_fare}")

    # Build the pdfunite command
    command = ["pdfunite"] + input_paths + [output_path]
    
    try:
        subprocess.run(command, check=True)
        print(f"Successfully merged files into: {output_path}")
    except Exception as e:
        print(f"Error merging files: {e}")

if __name__ == "__main__":
    main()
