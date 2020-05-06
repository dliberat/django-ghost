from os import path
import re
import logging
import json

from .Trie import Trie

logger = logging.getLogger("ghostAppLogger")

###########################################################
# Output variables
###########################################################
EN_TRIE = None
EN_DEFINITIONS = None


###########################################################
# Load files
###########################################################

EN_WEBSTERS_WORDS_PATH = "static/game/wordlist.txt"
EN_WEBSTERS_DICT_PATH = "static/game/definitions.json"

en_word_list = []

logger.info(f"Loading EN words list from '{EN_WEBSTERS_WORDS_PATH}'")

with open(path.join(path.dirname(__file__), EN_WEBSTERS_WORDS_PATH)) as f:
  line = f.readline().strip().lower()
  while line:
    match = re.match(r"^[a-zA-Z]*$", line) 
    if match is not None:
      en_word_list.append(line)
    else:
      logger.error(f"File contains invalid token: '{line}'")
    line = f.readline().strip().lower()

logger.info(f"Loaded {len(en_word_list)} words from file.")

EN_TRIE = Trie()
EN_TRIE.insert_all(en_word_list)

logger.info("Built EN trie.")


logger.info(f"Loading full EN dictionary from '{EN_WEBSTERS_DICT_PATH}'")
with open(path.join(path.dirname(__file__), EN_WEBSTERS_DICT_PATH)) as f:
  EN_DEFINITIONS = json.load(f)
logger.info("Loaded full EN dictionary.")