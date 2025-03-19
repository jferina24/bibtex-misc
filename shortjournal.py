# This code was AI-assisted
# It uses a file of common IEEE abbreviations to create a short journal field in a Bibtex entry
import re

# Path to the used references BibTeX file
used_bibtex_file = 'output (1).bib'

def read_abbreviations(file_path):
    abbreviations = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Strip any leading/trailing whitespace from the line
            line = line.strip()
           
            # Split the line on tabs
            parts = line.split('\t')
            # Check if the line has more than 2 strings of text
            if len(parts) > 1:
                key = parts[0].strip()
                value = parts[1].strip()
                abbreviations[key] = value
                # Handle keys with parentheses
                if '(' in key and ')' in key:
                    # Add the version without the parentheses content
                    key_without_parens = re.sub(r'\([^)]*\)', '', key).strip()
                    key_with_parens = key.replace('(', '')
                    key_with_parens = key_with_parens.replace(')','')
                    abbreviations[key_without_parens] = value
                    abbreviations[key_with_parens] = value
    
    return abbreviations


# Example usage
file_path = 'ieee_abbrev.txt'
ieee_abbreviations = read_abbreviations(file_path)
ieee_abbreviations['Disorder'] = 'Disord.'
ieee_abbreviations['Disorders'] = 'Disord.'
ieee_abbreviations['Disabilities'] = 'Disabil.'
ieee_abbreviations['Physical'] = 'Phys.'
ieee_abbreviations['Frontiers'] = 'Front.'
#ieee_abbreviations['Autism'] = "Aut."

# List of prepositions to remove from shortjournal names
prepositions = ["of", "the", "and", "in", "for", "with", "on", "by", "to"]

# Function to remove prepositions from a string
def remove_prepositions(name):
    words = name.split()
    return ' '.join(word for word in words if word.lower() not in prepositions)

# Read the used references BibTeX file
with open(used_bibtex_file, 'r', encoding='utf-8') as file:
    bibtex_content = file.read()

# Split the BibTeX entries based on "@{"
bib_entries = re.split(r'(?=@\w+\{)', bibtex_content)
print(len(bib_entries))


# Process each entry to add shortjournal if missing
updated_entries = []
for entry in bib_entries:
    # Check if the entry is not empty and if it already has a shortjournal field
    if entry.strip() and "shortjournal" not in entry:
        
        # Extract the journal or journaltitle name with flexible spacing around the equals sign
        match = re.search(r'(?:journal|journaltitle|booktitle|eventtitle)\s*=\s*{([^}]*)}', entry)
#re.search(r'journal(?:title)?\s*=\s*{([^}]*)}', entry)
        if match:
            journal_name = match.group(1)
            journal_name = journal_name.replace("{", "").replace("}", "")
            jn = []
            for word in journal_name.split():
                if word.lower() in prepositions:
                    jn.append(word)
                    continue

                if re.match(r'^\d+', word):
                    jn.append(word)
                    continue
                
                if not word.isupper():
                    jn.append(word.title())
                else:
                    jn.append(word)
            journal_name = " ".join(jn)
            short_journal =[]
            # Find the IEEE abbreviation
            for word in journal_name.split():
                short_journal.append(ieee_abbreviations.get(word,word))
            
            short_journal = " ".join(short_journal)

            # Remove prepositions from the short journal name
            short_journal = remove_prepositions(short_journal)
            print(short_journal)
            # Add the shortjournal field to the entry
            entry = re.sub(r'journal(?:title)?\s*=\s*{([^}]*)}', f'journal = {{{journal_name}}}', entry)
            entry = re.sub(r'(\n})', f',\n  shortjournal = {{{short_journal}}}\n}}', entry)#re.sub(r'}\s*\n', f',\n  shortjournal = {{{short_journal}}}\n}}\n', entry)
            # proceedings title to shortened title
    updated_entries.append(entry)

final_content = '\n\n'.join(updated_entries)
final_content = re.sub(r',\s*,', ',', final_content)
new_bibtex_file = "updated_references.bib"
# Write the updated entries back to the BibTeX file
with open(new_bibtex_file, 'w', encoding='utf-8') as file:
    file.write(final_content)

print(f'Updated BibTeX file saved as {new_bibtex_file}')
