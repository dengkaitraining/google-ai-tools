import os
import re
import shutil
import pypdf

def extract_ticket_info(pdf_path):
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return None

    lines = [line.strip() for line in text.split("\n")]
    
    date_str = None
    dep_time = None
    price = None
    
    # 1. Travel Date: look for line that is exactly YYYY/MM/DD
    dates = []
    for line in lines:
        match = re.match(r"^(\d{4})/(\d{2})/(\d{2})$", line)
        if match:
            dates.append(match.groups())
            
    if dates:
        yyyy, mm, dd = dates[0]
        date_str = f"{yyyy}{mm}{dd}"
        
    # 2. Departure Time: from the itinerary line containing HH:MM - HH:MM
    for line in lines:
        time_matches = re.findall(r"(\d{2}):(\d{2})", line)
        if time_matches and " - " in line:
            hh, mm = time_matches[0]
            dep_time = f"{hh}{mm}"
            break
            
    # 3. Fare: look for NT$ XXX
    for line in lines:
        match = re.match(r"^NT\$\s*(\d+)$", line)
        if match:
            price = match.group(1)
            break
            
    if date_str and dep_time and price:
        return {
            "date": date_str,
            "time": dep_time,
            "price": price
        }
    else:
        print(f"Warning: could not find all info in {pdf_path}: date={date_str}, time={dep_time}, price={price}")
        return None

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
