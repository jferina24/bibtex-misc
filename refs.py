# This code was AI-assisted
# It takes a folder of multiple bib files and an aux file, and combines bib files into one
# Based on the aux file, it removes citation keys that are unused.

import os
import re

# Paths to the files
bib_folder = 'bibs'
aux_file = 'output (1).aux'
combined_bibtex_file = 'combined.bib'
new_bibtex_file = 'used_references.bib'

# Combine all .bib files into one
with open(combined_bibtex_file, 'wb') as combined_bib:
    for filename in os.listdir(bib_folder):
        if filename.endswith('.bib'):
            with open(os.path.join(bib_folder, filename), 'rb') as bib_file:
                combined_bib.write(bib_file.read())
                combined_bib.write(b'\n')

# Read the combined BibTeX file
with open(combined_bibtex_file, 'rb') as bibtex:
    combined_bib_content = bibtex.read().decode('utf-8', errors='ignore')
print(f'Combined BibTeX file size: {len(combined_bib_content)} bytes')

# Extract citation keys from the .aux file
with open(aux_file, 'r', encoding='utf-8') as aux:
    aux_content = aux.read()
citation_keys = set(re.findall(r'\\abx@aux@(?:cite|segm){[^}]*}{([^}]*)}', aux_content))
print(f'Number of citation keys extracted: {len(citation_keys)}')

# Extract used references from the combined BibTeX file
used_references = []
for key in citation_keys:
    #pattern = rf'@.*?{{\s*{key}\s*,.*?}}(?=\s*@|$)'#rf'@.*?{{\s*{key}\s*,.*?}}\n'  # Adjusted regex pattern
    print(key)
    pattern = rf'@[\w]+\{{{re.escape(key)}\s*,[\s\S]*?}}(?=\s*@|\s*$)'
    match = re.search(pattern, combined_bib_content, re.DOTALL)
    if match:
        used_references.append(match.group())
        #print(match.group())
        #print(key)
        #raise ValueError()
    # else:
    #     raise ValueError("no match")

# Write the used references to the new BibTeX file
with open(new_bibtex_file, 'wb') as new_bib:
    new_bib.write('\n'.join(used_references).encode('utf-8'))

# Output the size of the used references file
print(f'Filtered BibTeX file size: {os.path.getsize(new_bibtex_file)} bytes')

print(f'Filtered BibTeX file saved as {new_bibtex_file}')
