from django.http import JsonResponse, HttpResponseBadRequest
import re
import logging

from .asset_loader import EN_TRIE, EN_DEFINITIONS
from .GhostGame import GhostGame

logger = logging.getLogger("ghostAppLogger")

logger.info("Starting up game instance")
game = GhostGame(EN_TRIE)


def validate_word(word):
    return word is not None and re.match(r"^[a-zA-Z]*$", word) is not None


def index(request):

    logger.debug("Received request.")

    current_word = request.GET.get('word', None)

    if not validate_word(current_word):
        logger.info(f"Rejected invalid word: {current_word}")
        return HttpResponseBadRequest("Word must be a string of letters.")
    
    current_word = current_word.lower()
    logger.debug(f"Parsed word from request: {current_word}")

    cpu_move = game.make_move(current_word)

    res = dict()
    res['is_game_over'] = cpu_move.is_game_over
    res['previous_word'] = current_word
    res['cpu_word'] = cpu_move.word
    res['is_real_word'] = cpu_move.is_real_word
    res['definition'] = None

    if cpu_move.is_game_over:
        target_word = cpu_move.word if cpu_move.word is not None else current_word
        target_word = target_word.lower()
        if target_word in EN_DEFINITIONS:
            res['definition'] = EN_DEFINITIONS[target_word]

    return JsonResponse(res)