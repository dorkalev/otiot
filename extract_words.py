import csv
import re
import json
from collections import Counter

# Common English stopwords to filter out
STOPWORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
    'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been', 'be', 'have',
    'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
    'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
    'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your',
    'his', 'its', 'our', 'their', 'what', 'which', 'who', 'whom', 'when', 'where',
    'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
    'very', 's', 't', 'd', 'm', 've', 'll', 're', 'am', 'if', 'then', 'else',
    'just', 'about', 'into', 'over', 'after', 'before', 'up', 'down', 'out', 'off',
    'above', 'below', 'between', 'under', 'again', 'further', 'once', 'here', 'there',
    'any', 'because', 'during', 'through', 'until', 'while', 'against', 'being',
    'having', 'doing', 'said', 'get', 'got', 'go', 'going', 'went', 'come', 'came',
    'coming', 'make', 'made', 'take', 'took', 'let', 'see', 'saw', 'seen', 'look',
    'looked', 'looking', 'back', 'now', 'way', 'even', 'well', 'also', 'around',
    'still', 'know', 'knew', 'think', 'thought', 'tell', 'told', 'ask', 'asked',
    'put', 'give', 'gave', 'find', 'found', 'want', 'wanted', 'seem', 'seemed',
    'feel', 'felt', 'try', 'tried', 'leave', 'left', 'call', 'called', 'keep',
    'kept', 'need', 'needed', 'mean', 'meant', 'turn', 'turned', 'start', 'started',
    'show', 'showed', 'hear', 'heard', 'play', 'played', 'run', 'ran', 'move',
    'moved', 'live', 'lived', 'believe', 'hold', 'held', 'bring', 'brought',
    'happen', 'happened', 'write', 'wrote', 'sit', 'sat', 'stand', 'stood', 'lose',
    'lost', 'pay', 'paid', 'meet', 'met', 'include', 'continue', 'set', 'learn',
    'learned', 'change', 'changed', 'lead', 'led', 'understand', 'understood',
    'watch', 'watched', 'follow', 'followed', 'stop', 'stopped', 'create', 'speak',
    'spoke', 'read', 'allow', 'add', 'added', 'spend', 'spent', 'grow', 'grew',
    'open', 'opened', 'walk', 'walked', 'win', 'won', 'offer', 'offered', 'remember',
    'remembered', 'love', 'loved', 'consider', 'appear', 'appeared', 'buy', 'bought',
    'wait', 'waited', 'serve', 'served', 'die', 'died', 'send', 'sent', 'expect',
    'expected', 'build', 'built', 'stay', 'stayed', 'fall', 'fell', 'cut', 'reach',
    'reached', 'kill', 'killed', 'remain', 'remained', 'suggest', 'raise', 'raised',
    'pass', 'passed', 'sell', 'sold', 'require', 'report', 'reported', 'decide',
    'decided', 'pull', 'pulled', 'push', 'pushed'
}

# Read the CSV
with open('harry_potter_books.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    # Filter for Book 1 only and concat all text
    book1_text = []
    for row in reader:
        if "Philosopher's Stone" in row['book']:
            book1_text.append(row['text'])

# Join all text
full_text = ' '.join(book1_text)

# Clean up: remove punctuation, quotes, hyphens, etc.
cleaned = re.sub(r'[^a-zA-Z\s]', ' ', full_text)
cleaned = cleaned.lower()

# Split into words and filter empty strings
words = [w.strip() for w in cleaned.split() if w.strip()]

# Find unique words
unique_words = sorted(set(words))

# Count frequencies
word_counts = Counter(words)

# Filter: remove stopwords, single letters, and very short words
meaningful_words = [
    w for w in unique_words
    if w not in STOPWORDS
    and len(w) > 2
    and not w.isdigit()
]

print(f"Total words in Book 1: {len(words)}")
print(f"Unique words: {len(unique_words)}")
print(f"Meaningful words (after filtering): {len(meaningful_words)}")

# Save to JSON for further processing
with open('hp_words.json', 'w', encoding='utf-8') as f:
    json.dump(meaningful_words, f, indent=2)

print(f"\nSaved {len(meaningful_words)} words to hp_words.json")

# Also save with frequencies
words_with_freq = [
    {"word": w, "count": word_counts[w]}
    for w in meaningful_words
]
words_with_freq.sort(key=lambda x: -x['count'])

with open('hp_words_freq.json', 'w', encoding='utf-8') as f:
    json.dump(words_with_freq, f, indent=2)

print(f"Saved words with frequencies to hp_words_freq.json")

# Show sample
print(f"\nTop 100 most frequent meaningful words:")
for item in words_with_freq[:100]:
    print(f"  {item['word']}: {item['count']}")
