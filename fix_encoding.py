import codecs

# Read original content
with open('tests/test_symbol_texts/test_symbol_texts.asc', 'rb') as f:
    content = f.read()

# Convert to string, removing BOM if present
text = content.decode('utf-16')

# Make our modifications
lines = text.splitlines()
modified = False
for i, line in enumerate(lines):
    if line.startswith('SYMATTR InstName R1'):
        # Add value after instance name if not already there
        if i + 1 >= len(lines) or not lines[i + 1].startswith('SYMATTR Value'):
            lines.insert(i + 1, 'SYMATTR Value 10k')
            modified = True
    elif line.startswith('SYMATTR InstName X9'):
        if i + 1 >= len(lines) or not lines[i + 1].startswith('SYMATTR Value'):
            lines.insert(i + 1, 'SYMATTR Value CS_nMOS')
            modified = True
    elif line.startswith('SYMATTR InstName C1'):
        if i + 1 >= len(lines) or not lines[i + 1].startswith('SYMATTR Value'):
            lines.insert(i + 1, 'SYMATTR Value 1u')
            modified = True

# Write back with proper encoding
with open('tests/test_symbol_texts/test_symbol_texts.asc', 'w', encoding='utf-16le') as f:
    f.write('\n'.join(lines)) 