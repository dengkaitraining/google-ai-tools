import os
import re
import subprocess
import shutil

def extract_ticket_info(pdf_path):
    try:
        # Run pdftotext to extract text content
        result = subprocess.run(
            ["pdftotext", pdf_path, "-"],
            capture_output=True,
            text=True,
            check=True
        )
        text = result.stdout
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return None

    # 1. Extract Travel Date (乘車日期)
    # Pattern: 乘車日期 Travel Date followed by newlines and a YYYY/MM/DD date
    date_match = re.search(r"乘車日期\s*Travel\s*Date\s*[\r\n]+(?:\s*[\r\n]+)*\s*(\d{4})/(\d{2})/(\d{2})", text)
    if not date_match:
        # Fallback: look for any date YYYY/MM/DD in the text (though we prefer matching travel date explicitly)
        fallback_dates = re.findall(r"(\d{4})/(\d{2})/(\d{2})", text)
        if len(fallback_dates) >= 2:
            # High speed rail ticket typically has: Issue Date (開立日期) and Travel Date (乘車日期)
            # The travel date is usually the first or second depending on appearance.
            # Let's rely on the explicit match first.
            print(f"Warning: Travel Date pattern not found for {pdf_path}, using fallback.")
            # We'll just check if we can find Travel Date by another simpler pattern
            date_match = re.search(r"Travel\s*Date\s*[\r\n]+.*?(\d{4}/\d{2}/\d{2})", text, re.DOTALL)
            
    if date_match:
        yyyy, mm, dd = date_match.groups()
        date_str = f"{yyyy}{mm}{dd}"
    else:
        print(f"Could not find Travel Date in {pdf_path}")
        return None

    # 2. Extract Departure Time (出發時間) from Itinerary (區間)
    # Pattern: 區間 Itinerary followed by next line which has "HH:MM - HH:MM"
    itinerary_match = re.search(r"區間\s*Itinerary\s*[\r\n]+(?:\s*[\r\n]+)*\s*([^\r\n]+)", text)
    dep_time = None
    if itinerary_match:
        itinerary_line = itinerary_match.group(1)
        time_matches = re.findall(r"(\d{2}):(\d{2})", itinerary_line)
        if time_matches:
            hh, mm = time_matches[0]
            dep_time = f"{hh}{mm}"
            
    if not dep_time:
        print(f"Could not find Departure Time in {pdf_path}")
        return None

    # 3. Extract Fare (票價)
    # Pattern: 票款 Fare followed by NT$ XXXX
    fare_match = re.search(r"票款\s*Fare\s*[\r\n]+(?:\s*[\r\n]+)*\s*NT\$\s*(\d+)", text)
    if fare_match:
        price = fare_match.group(1)
    else:
        # Fallback
        fallback_fare = re.search(r"NT\$\s*(\d+)", text)
        if fallback_fare:
            price = fallback_fare.group(1)
        else:
            print(f"Could not find Ticket Price in {pdf_path}")
            return None

    return {
        "date": date_str,
        "time": dep_time,
        "price": price
    }

def main():
    tickets_dir = "Tickets"
    if not os.path.exists(tickets_dir):
        print(f"Error: Directory '{tickets_dir}' does not exist.")
        return

    # Find all PDF files
    pdf_files = [f for f in os.listdir(tickets_dir) if f.lower().endswith(".pdf")]
    
    processed_count = 0
    skipped_count = 0

    for filename in pdf_files:
        # Skip already renamed files to avoid processing copies or double renaming
        # Match pattern: [YYYYMMDD-HHMM][Price]OriginalName.pdf
        if re.match(r"^\[\d{8}-\d{4}\]\[\d+\].*", filename):
            print(f"Skipping already renamed file: {filename}")
            skipped_count += 1
            continue

        filepath = os.path.join(tickets_dir, filename)
        info = extract_ticket_info(filepath)
        
        if info:
            # Construct the new filename: [時間][票價]原檔名
            # Format: [YYYYMMDD-HHMM][Price]OriginalFilename
            time_part = f"{info['date']}-{info['time']}"
            new_filename = f"[{time_part}][{info['price']}]{filename}"
            new_filepath = os.path.join(tickets_dir, new_filename)
            
            # Copy file
            shutil.copy2(filepath, new_filepath)
            print(f"Successfully copied:\n  From: {filename}\n  To:   {new_filename}\n")
            processed_count += 1
        else:
            print(f"Failed to process: {filename}\n")

    print(f"Processing complete. {processed_count} files processed, {skipped_count} skipped.")

if __name__ == "__main__":
    main()
