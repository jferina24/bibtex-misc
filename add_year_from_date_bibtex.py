# This code was AI assisted
# The goal of this program is to add a year field from a date field in a Bibtex entry.


import re
import pandas as pd

def process_bib_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        bib_data = file.readlines()

    updated_bib = []
    entry = []
    for line in bib_data:
        if line.startswith("@"):
            if entry:
                updated_bib.append(process_entry(entry))
                entry = []
        entry.append(line)
    if entry:  # Process the last entry
        updated_bib.append(process_entry(entry))
    
    updated_bib = ''.join(updated_bib)
    with open(output_file, "w", encoding="utf-8") as file:
        file.writelines(updated_bib)

def process_entry(entry):
    entry_str = "".join(entry)

    print(entry_str)
    # Check if 'year' field exists
    if re.search(r"year\s*=", entry_str) is None:
        # Attempt to find the 'date' field
        date_match = re.search(r"\s*date\s*=\s*{(.*?)}", entry_str)
        print(date_match)
        if date_match:
            date_str = date_match.group(1)
            print(date_str)
            # Parse the date using pandas to extract the year
            try:
                # Handle cases where the date is just a year or a string of numbers starting with year
                year_match = re.match(r"(\d{4})", date_str)
                if year_match:
                    year = int(year_match.group(1))
                else:
                    year = pd.to_datetime(date_str).year
                
                # Insert 'year' field after the opening line
                for i, line in enumerate(entry):
                    if line.lstrip().startswith("title"):
                        entry.insert(i, f"  year = {{{year}}},\n")
                        break
            except ValueError:
                print(f"Error parsing date: {date_str}")
    return "".join(entry)

# Input and output file paths
input_bib_file = "references_old.bib"  # Replace with your input file name
output_bib_file = "output.bib"  # Replace with your desired output file name

# Process the BibTeX file
process_bib_file(input_bib_file, output_bib_file)

print(f"Processed BibTeX file saved to {output_bib_file}")