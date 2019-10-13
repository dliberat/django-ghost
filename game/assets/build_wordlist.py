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

# Dictionary file to create reduced files from
SRC_FILE = "en_websters_unabridged_full.json"

# This file will be used to provide word definitions
TGT_SHORT_DICT = "en_websters_unabridged.json"

# This file will be loaded into a Trie, and is used to determine endgame states
TGT_FILE = "en_websters_unabridged.txt"


# minimum word length is 4
pattern = re.compile("^[a-zA-Z]{4,}", re.ASCII)

def validate(word):
    return re.fullmatch(pattern, word) is not None


with open(path.join(path.dirname(__file__), SRC_FILE)) as f:
    dictionary = json.load(f)

# words only, no definitions
# no special characters (only a-z ascii)
# minimum length of 3
# lowercase only
wordlist = [key.lower() for key in dictionary if validate(key)]


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
    reduced_dict[word] = dictionary[word]

with open(path.join(path.dirname(__file__), TGT_SHORT_DICT), 'w') as f:
    json.dump(reduced_dict, f)