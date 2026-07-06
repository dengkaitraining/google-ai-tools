import os
import re
import pypdf

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

    # Sort chronologically by the time prefix (YYYYMMDD-HHMM)
    matching_files.sort()
    
    # Get the sorted list of file paths and calculate total fare
    input_paths = []
    print("Found files to merge (sorted chronologically):")
    for time_str, filename, price in matching_files:
        filepath = os.path.join(tickets_dir, filename)
        input_paths.append(filepath)
        total_fare += price
        print(f"  - {filename} (Fare: NT$ {price})")

    output_path = os.path.join(tickets_dir, "merged_tickets.pdf")

    # Merge PDFs using pypdf
    try:
        writer = pypdf.PdfWriter()
        for path in input_paths:
            writer.append(path)
        
        writer.write(output_path)
        writer.close()
        
        print(f"\nSuccessfully merged {len(input_paths)} files into: {output_path}")
        print(f"Total Fare (費用加總): NT$ {total_fare}")
    except Exception as e:
        print(f"Error merging files: {e}")

if __name__ == "__main__":
    main()
