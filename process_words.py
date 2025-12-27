import json
import re

# Load words
with open('hp_words_freq.json', 'r') as f:
    words_data = json.load(f)

# Known proper nouns / names from Harry Potter
PROPER_NOUNS = {
    'harry', 'ron', 'hagrid', 'hermione', 'snape', 'dumbledore', 'dudley',
    'malfoy', 'neville', 'vernon', 'quirrell', 'potter', 'mcgonagall',
    'gryffindor', 'hogwarts', 'petunia', 'dursley', 'dursleys', 'filch',
    'slytherin', 'weasley', 'draco', 'norbert', 'fluffy', 'hedwig',
    'oliver', 'seamus', 'dean', 'lavender', 'parvati', 'padma', 'percy',
    'fred', 'george', 'charlie', 'bill', 'ginny', 'molly', 'arthur',
    'crabbe', 'goyle', 'pansy', 'millicent', 'blaise', 'theodore',
    'hufflepuff', 'ravenclaw', 'godric', 'salazar', 'helga', 'rowena',
    'voldemort', 'riddle', 'tom', 'lily', 'james', 'sirius', 'remus',
    'peter', 'pettigrew', 'lupin', 'black', 'granger', 'longbottom',
    'sprout', 'flitwick', 'binns', 'trelawney', 'hooch', 'pomfrey',
    'pince', 'kettleburn', 'sinistra', 'vector', 'burbage', 'firenze',
    'diagon', 'alley', 'gringotts', 'ollivander', 'ollivanders',
    'flourish', 'blotts', 'leaky', 'cauldron', 'knockturn', 'borgin',
    'burkes', 'hogsmeade', 'honeydukes', 'zonko', 'shrieking', 'shack',
    'london', 'england', 'surrey', 'privet', 'drive', 'little', 'whinging',
    'nicolas', 'flamel', 'perenelle', 'griphook', 'scabbers', 'trevor',
    'errol', 'pigwidgeon', 'crookshanks', 'fang', 'buckbeak', 'aragog',
    'fawkes', 'dobby', 'kreacher', 'winky', 'nearly', 'headless', 'nick',
    'myrtle', 'peeves', 'bloody', 'baron', 'fat', 'friar', 'grey', 'lady',
    'binky', 'nimbus', 'firebolt', 'cleansweep', 'comet', 'shooting', 'star',
    'remembrall', 'deluminator', 'pensieve', 'horcrux', 'hallows', 'elder',
    'resurrection', 'invisibility', 'marauder', 'map', 'mirror', 'erised',
    'sorcerer', 'philosopher', 'azkaban', 'dementor', 'dementors',
    'ministry', 'muggle', 'muggles', 'quidditch', 'seeker', 'chaser',
    'beater', 'keeper', 'snitch', 'bludger', 'bludgers', 'quaffle',
    'bertie', 'bott', 'botts', 'chocolate', 'frog', 'frogs', 'pumpkin',
    'pasty', 'pasties', 'butterbeer', 'firewhisky', 'gillywater',
    'polyjuice', 'veritaserum', 'amortentia', 'felix', 'felicis',
    'wolfsbane', 'skele', 'gro', 'pepperup', 'mandrake', 'mandragora',
    'bezoar', 'bicorn', 'boomslang', 'gillyweed', 'mimbulus', 'mimbletonia',
    'venomous', 'tentacula', 'whomping', 'willow', 'forbidden', 'forest',
    'chamber', 'secrets', 'room', 'requirement', 'astronomy', 'tower',
    'owlery', 'hospital', 'wing', 'great', 'hall', 'entrance', 'dungeon',
    'dungeons', 'greenhouse', 'greenhouses', 'quidditch', 'pitch', 'field',
    'ground', 'grounds', 'lake', 'black', 'squid', 'merpeople', 'grindylow',
    'grindylows', 'hippogriff', 'hippogriffs', 'thestral', 'thestrals',
    'phoenix', 'basilisk', 'acromantula', 'centaur', 'centaurs', 'unicorn',
    'unicorns', 'werewolf', 'werewolves', 'vampire', 'vampires', 'ghost',
    'ghosts', 'boggart', 'boggarts', 'pixie', 'pixies', 'gnome', 'gnomes',
    'goblin', 'goblins', 'house', 'elf', 'elves', 'giant', 'giants',
    'troll', 'trolls', 'dragon', 'dragons', 'norwegian', 'ridgeback',
    'hungarian', 'horntail', 'welsh', 'green', 'swedish', 'short', 'snout',
    'common', 'antipodean', 'opaleye', 'peruvian', 'vipertooth', 'romanian',
    'longhorn', 'ukrainian', 'ironbelly', 'hebridean', 'norberta',
    'expelliarmus', 'stupefy', 'petrificus', 'totalus', 'impedimenta',
    'reducto', 'diffindo', 'incendio', 'aguamenti', 'lumos', 'nox',
    'alohomora', 'colloportus', 'reparo', 'scourgify', 'tergeo', 'accio',
    'wingardium', 'leviosa', 'locomotor', 'mortis', 'mobiliarbus',
    'mobilicorpus', 'expecto', 'patronum', 'riddikulus', 'obliviate',
    'confundo', 'imperio', 'crucio', 'avada', 'kedavra', 'sectumsempra',
    'levicorpus', 'liberacorpus', 'muffliato', 'protego', 'salvio',
    'hexia', 'cave', 'inimicum', 'repello', 'muggletum', 'fianto', 'duri',
    'protean', 'fidelius', 'taboo', 'trace', 'apparate', 'apparition',
    'disapparate', 'disapparition', 'portkey', 'floo', 'powder', 'network',
    'animagus', 'animagi', 'metamorphmagus', 'metamorphmagi', 'parselmouth',
    'parselmouths', 'parseltongue', 'legilimency', 'legilimens',
    'occlumency', 'occlumens', 'seer', 'seers', 'prophecy', 'prophecies',
    'divination', 'arithmancy', 'runes', 'muggle', 'studies', 'care',
    'magical', 'creatures', 'herbology', 'potions', 'transfiguration',
    'charms', 'defense', 'dark', 'arts', 'history', 'magic', 'flying',
    'apparition', 'alchemy', 'ancient', 'astronomy', 'newt', 'newts',
    'owl', 'owls', 'acceptable', 'exceeds', 'expectations', 'outstanding',
    'poor', 'dreadful', 'troll', 'prefect', 'prefects', 'head', 'boy',
    'girl', 'quidditch', 'captain', 'seeker', 'chaser', 'beater', 'keeper',
    'galleon', 'galleons', 'sickle', 'sickles', 'knut', 'knuts',
    'daily', 'prophet', 'quibbler', 'witch', 'weekly', 'evening', 'standard',
    'wireless', 'network', 'weird', 'sisters', 'celestina', 'warbeck',
    'howler', 'howlers', 'howl', 'howling', 'patronus', 'patroni',
    'corporeal', 'non', 'dementor', 'kiss', 'chocolate', 'frog', 'card',
    'cards', 'wizard', 'witches', 'wizards', 'muggle', 'born', 'half',
    'blood', 'pure', 'squib', 'squibs', 'mudblood', 'mudbloods',
    'death', 'eater', 'eaters', 'order', 'phoenix', 'army', 'ministry',
    'auror', 'aurors', 'hit', 'wizard', 'unspeakable', 'unspeakables',
    'obliviator', 'obliviators', 'healer', 'healers', 'medi', 'witch',
    'curse', 'breaker', 'breakers', 'dragonologist', 'dragonologists',
    'magizoologist', 'magizoologists', 'wandmaker', 'wandmakers',
    'apothecary', 'apothecaries', 'weasleys', 'wizard', 'wheezes',
    'zonko', 'joke', 'shop', 'florean', 'fortescue', 'ice', 'cream',
    'parlor', 'eeylops', 'emporium', 'magical', 'menagerie', 'quality',
    'supplies', 'slug', 'jiggers', 'twilfitt', 'tattings', 'madam',
    'malkin', 'malkins', 'robes', 'occasions', 'rosa', 'lee', 'jordan',
    'angelina', 'johnson', 'alicia', 'spinnet', 'katie', 'bell', 'colin',
    'creevey', 'dennis', 'nigel', 'romilda', 'vane', 'cormac', 'mclaggen',
    'ernie', 'macmillan', 'hannah', 'abbott', 'justin', 'finch', 'fletchley',
    'susan', 'bones', 'zacharias', 'smith', 'terry', 'boot', 'anthony',
    'goldstein', 'michael', 'corner', 'luna', 'lovegood', 'cho', 'chang',
    'marietta', 'edgecombe', 'roger', 'davies', 'cedric', 'diggory',
    'viktor', 'krum', 'fleur', 'delacour', 'gabrielle', 'olympe', 'maxime',
    'igor', 'karkaroff', 'ludovic', 'ludo', 'bagman', 'barty', 'crouch',
    'cornelius', 'fudge', 'rufus', 'scrimgeour', 'pius', 'thicknesse',
    'kingsley', 'shacklebolt', 'nymphadora', 'tonks', 'andromeda',
    'narcissa', 'bellatrix', 'lestrange', 'rodolphus', 'rabastan',
    'regulus', 'arcturus', 'orion', 'walburga', 'phineas', 'nigellus',
    'armando', 'dippet', 'headmistress', 'headmaster', 'deputy',
    'minerva', 'severus', 'albus', 'percival', 'wulfric', 'brian',
    'horace', 'slughorn', 'gilderoy', 'lockhart', 'remus', 'john',
    'lupin', 'alastor', 'moody', 'bartemius', 'dolores', 'jane', 'umbridge',
    'amycus', 'alecto', 'carrow', 'rolanda', 'pomona', 'filius', 'cuthbert',
    'aurora', 'septima', 'bathsheda', 'babbling', 'charity', 'rubeus',
    'silvanus', 'wilhelmina', 'grubbly', 'plank', 'sybill', 'patricia',
    'trelawney', 'argus', 'irma', 'poppy', 'madam', 'rosmerta', 'aberforth',
    'ariana', 'kendra', 'percival', 'gellert', 'grindelwald', 'bathilda',
    'bagshot', 'gregorovitch', 'xenophilius', 'pandora', 'selwyn', 'yaxley',
    'rookwood', 'augustus', 'mulciber', 'avery', 'nott', 'mcnair', 'walden',
    'travers', 'jugson', 'dolohov', 'antonin', 'rowle', 'thorfinn', 'gibbon',
    'fenrir', 'greyback', 'scabior', 'wormtail', 'padfoot', 'prongs', 'moony',
    # Hagrid's dialect
    'yeh', 'yer', 'ter', 'fer', 'inter', 'outta', 'sorta', 'kinda',
    'gotta', 'wanna', 'gonna', 'dunno', 'summat', 'nuthin', 'somethin',
    'nothin', 'anythin', 'everythin',
    # Contractions fragments
    'didn', 'don', 'couldn', 'wouldn', 'shouldn', 'wasn', 'weren', 'isn',
    'aren', 'hasn', 'haven', 'hadn', 'won', 'ain', 'shan', 'mustn', 'needn',
    # Made up words
    'undursleyish', 'quidditch'
}

# Separate words
proper_nouns = []
regular_words = []
contractions = []

for item in words_data:
    word = item['word']
    if word in PROPER_NOUNS or word.endswith('s') and word[:-1] in PROPER_NOUNS:
        proper_nouns.append(item)
    elif word in {'didn', 'don', 'couldn', 'wouldn', 'shouldn', 'wasn', 'weren',
                  'isn', 'aren', 'hasn', 'haven', 'hadn', 'won', 'ain', 'shan'}:
        contractions.append(item)
    else:
        regular_words.append(item)

print(f"Proper nouns/names: {len(proper_nouns)}")
print(f"Contractions: {len(contractions)}")
print(f"Regular words for translation: {len(regular_words)}")

# Save regular words
with open('hp_regular_words.json', 'w', encoding='utf-8') as f:
    json.dump(regular_words, f, indent=2)

print(f"\nSaved {len(regular_words)} regular words to hp_regular_words.json")

# Show sample of regular words
print(f"\nTop 50 regular words:")
for item in regular_words[:50]:
    print(f"  {item['word']}: {item['count']}")
