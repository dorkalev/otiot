import json
from translations import TRANSLATIONS
from translations_extra import EXTRA_TRANSLATIONS
from translations_more import MORE_TRANSLATIONS
from translations_complete import COMPLETE_TRANSLATIONS
from translations_final import FINAL_TRANSLATIONS
from translations_remaining import REMAINING_TRANSLATIONS
from translations_last import LAST_TRANSLATIONS

# Harry Potter proper nouns with Hebrew transliterations
PROPER_NOUNS = {
    # Main characters
    'harry': 'הארי',
    'potter': 'פוטר',
    'ron': 'רון',
    'weasley': 'ויזלי',
    'hermione': 'הרמיוני',
    'granger': 'גריינג\'ר',
    'hagrid': 'האגריד',
    'dumbledore': 'דמבלדור',
    'snape': 'סנייפ',
    'mcgonagall': 'מקגונגל',
    'voldemort': 'וולדמורט',
    'quirrell': 'קווירל',

    # Dursleys
    'dudley': 'דאדלי',
    'vernon': 'ורנון',
    'petunia': 'פטוניה',
    'dursley': 'דרסלי',
    'dursleys': 'משפחת דרסלי',

    # Students
    'neville': 'נוויל',
    'longbottom': 'לונגבוטום',
    'malfoy': 'מאלפוי',
    'draco': 'דראקו',
    'crabbe': 'קראב',
    'goyle': 'גויל',
    'seamus': 'שיימוס',
    'dean': 'דין',
    'lavender': 'לבנדר',
    'parvati': 'פרווטי',
    'fred': 'פרד',
    'george': 'ג\'ורג\'',
    'percy': 'פרסי',
    'oliver': 'אוליבר',
    'wood': 'ווד',

    # Staff
    'filch': 'פילץ\'',
    'sprout': 'ספראוט',
    'flitwick': 'פליטוויק',
    'binns': 'בינס',
    'hooch': 'הוץ\'',
    'pomfrey': 'פומפרי',
    'pince': 'פינס',

    # Houses
    'gryffindor': 'גריפינדור',
    'slytherin': 'סלית\'רין',
    'hufflepuff': 'האפלפאף',
    'ravenclaw': 'רייבנקלו',

    # Places
    'hogwarts': 'הוגוורטס',
    'diagon': 'סמטת דיאגון',
    'gringotts': 'גרינגוטס',
    'london': 'לונדון',
    'england': 'אנגליה',
    'privet': 'פריווט',

    # Other characters
    'nicolas': 'ניקולס',
    'flamel': 'פלאמל',
    'norbert': 'נורברט',
    'hedwig': 'הדוויג',
    'scabbers': 'סקאברס',
    'trevor': 'טרוור',
    'fang': 'פאנג',
    'fluffy': 'פלאפי',
    'peeves': 'פיבס',
    'nearly': 'כמעט',
    'nick': 'ניק',

    # Items & Concepts (keep as loan words)
    'quidditch': 'קווידיץ\'',
    'muggle': 'מוגל',
    'muggles': 'מוגלים',
}

# Load words from file
with open('hp_words_freq.json', 'r') as f:
    words_data = json.load(f)

# Combine all translations
ALL_TRANSLATIONS = {**TRANSLATIONS, **EXTRA_TRANSLATIONS, **MORE_TRANSLATIONS, **COMPLETE_TRANSLATIONS, **FINAL_TRANSLATIONS, **REMAINING_TRANSLATIONS, **LAST_TRANSLATIONS, **PROPER_NOUNS}

# Generate vocabulary with translations
vocabulary = []
missing_words = []

for item in words_data:
    word = item['word']
    count = item['count']

    if word in ALL_TRANSLATIONS:
        vocabulary.append({
            'english': word,
            'hebrew': ALL_TRANSLATIONS[word],
            'frequency': count
        })
    else:
        missing_words.append({'word': word, 'count': count})

# Sort by frequency
vocabulary.sort(key=lambda x: -x['frequency'])

print(f"Total words with translations: {len(vocabulary)}")
print(f"Missing translations: {len(missing_words)}")

# Save vocabulary
with open('hp_vocabulary.json', 'w', encoding='utf-8') as f:
    json.dump(vocabulary, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(vocabulary)} words to hp_vocabulary.json")

# Save missing words for review
with open('hp_missing_words.json', 'w', encoding='utf-8') as f:
    json.dump(missing_words, f, ensure_ascii=False, indent=2)

print(f"Saved {len(missing_words)} missing words to hp_missing_words.json")

# Show sample
print(f"\nTop 50 translated words:")
for item in vocabulary[:50]:
    print(f"  {item['english']}: {item['hebrew']} ({item['frequency']})")

print(f"\nTop 50 missing words:")
for item in missing_words[:50]:
    print(f"  {item['word']}: {item['count']}")
