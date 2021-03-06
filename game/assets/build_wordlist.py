###############################################################################
# This script converts a dictionary in json form (where keys are words
# and values are their definitions) into two smaller files that are loaded
# by the server when it boots.
#
# The smaller files represent the words and definitions that will
# be used throughout gameplay.
#
# This script (or some variant of it) may be run when updating or
# providing a new dictionary.
#
# Because of the specific game rules, there are a lot of optimizations
# that can be made to the full dictionary in order to reduce the
# size of the data structures. For example, all words shorter than
# four characters do not need to be saved since the game rules
# allow words of up to 3 characters to be played without penalty.
# (Note: In the GhostGame implementation, this rule is not actually
# implemented within the game logic. The GhostGame class relies on
# its wordlist Trie to simply not include words which would not
# constitute an endgame condition.)
#
###############################################################################

from os import path
import json
import re

# Word list
WORD_LIST = "gutenberg_top_10000.txt"

# Word definitions
SRC_FILE = "en_websters_unabridged_full.json"

# Output file for endgame states
TGT_FILE = "wordlist.txt"

# Output file for definitions
TGT_SHORT_DICT = "definitions.json"

# minimum word length is 4
pattern = re.compile("^[a-zA-Z]{4,}$")

def validate(word):
    return re.match(pattern, word) is not None

with open(path.join(path.dirname(__file__), SRC_FILE)) as f:
    dictionary = json.load(f)

with open(path.join(path.dirname(__file__), WORD_LIST)) as f:
    wordlist = [key.lower().strip() for key in f.readlines() if validate(key)]


if not wordlist:
    print("Error. No words have been loaded.")
    exit()
elif len(wordlist) < 2:
    print("Error. Only one word has been loaded.")
    exit()

###############################################################################
# Remove all long words whose substrings are also words,
# since the short word will be reached first and the game
# will end before the longer word can ever be reached
###############################################################################
wordlist.sort()

reduced_wordlist = wordlist[0:1]

prev = wordlist[0]
current = wordlist[1]

for i in range(1, len(wordlist)):
    if not current.startswith(prev):
        reduced_wordlist.append(current)
        prev = current
    current = wordlist[i]


# one last iteration to catch the final word in the dictionary
if not current.startswith(prev):
    reduced_wordlist.append(current)

###############################################################################
# Create wordlist to be loaded into the Trie
###############################################################################
with open(path.join(path.dirname(__file__), TGT_FILE), 'w') as f:
    for word in reduced_wordlist:
        f.write(word + "\n")


###############################################################################
# Create reduced dictionary that only contains the words that exist
# in the wordlist.
###############################################################################

reduced_dict = dict()
for word in reduced_wordlist:
    definition = dictionary.get(word, None)
    if definition is not None:
        reduced_dict[word] = definition

with open(path.join(path.dirname(__file__), TGT_SHORT_DICT), 'w') as f:
    json.dump(reduced_dict, f)