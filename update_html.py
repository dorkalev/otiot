import re

# Read the original HTML file
with open('harry-potter.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Read the new vocabulary
with open('hp_vocabulary.js', 'r', encoding='utf-8') as f:
    new_vocab = f.read()

# Find and replace the vocabulary section
# Pattern to match the old vocabulary array
pattern = r"        // Harry Potter and the Philosopher's Stone vocabulary\n        // English words with Hebrew translations\n        const vocabulary = \[.*?\];"

# Replace with new vocabulary (using DOTALL to match across lines)
new_html = re.sub(pattern, new_vocab, html_content, flags=re.DOTALL)

# Write the updated HTML
with open('harry-potter.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Updated harry-potter.html with new vocabulary")

# Verify
with open('harry-potter.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Count vocabulary entries
vocab_count = content.count("{ english:")
print(f"Vocabulary entries in HTML: {vocab_count}")
