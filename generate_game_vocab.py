import json

# Load the vocabulary
with open('hp_vocabulary.json', 'r', encoding='utf-8') as f:
    vocabulary = json.load(f)

# Generate JavaScript array
js_lines = ["        // Harry Potter and the Philosopher's Stone vocabulary"]
js_lines.append(f"        // {len(vocabulary)} unique words with Hebrew translations")
js_lines.append("        const vocabulary = [")

for item in vocabulary:
    english = item['english'].replace("'", "\\'")
    hebrew = item['hebrew'].replace("'", "\\'")
    js_lines.append(f"            {{ english: '{english}', hebrew: '{hebrew}' }},")

js_lines.append("        ];")

# Write to file
output = '\n'.join(js_lines)

with open('hp_vocabulary.js', 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Generated JavaScript vocabulary with {len(vocabulary)} words")
print(f"Saved to hp_vocabulary.js")

# Show first 20 and last 20 lines
print("\nFirst 25 entries:")
for item in vocabulary[:25]:
    print(f"  {item['english']}: {item['hebrew']}")

print("\nLast 10 entries:")
for item in vocabulary[-10:]:
    print(f"  {item['english']}: {item['hebrew']}")
