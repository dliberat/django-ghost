from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render

import re

from .asset_loader import EN_TRIE, EN_DEFINITIONS
from .GhostGame import GhostGame

game = GhostGame(EN_TRIE)


def validate_word(word):
    return word is not None and re.match(r"^[a-zA-Z]*$", word) is not None


def index(request):
    ctx = {}

    if request.method == 'POST':
        
        if request.POST.get('reset', None) is not None:
            ctx['prefix'] = ''
        else:
            usr_input = request.POST.get('input-txt', '')
            prefix = request.POST.get('prefix', '') + usr_input
            prefix = prefix.lower()

            if not validate_word(prefix):
                logger.info(f"Rejected invalid word: {prefix}")
                return HttpResponseBadRequest("Word must be a string of letters.")

            cpu_move = game.make_move(prefix)
            ctx['is_game_over'] = cpu_move.is_game_over
            ctx['previous_word'] = prefix
            ctx['prefix'] = cpu_move.word
            ctx['is_real_word'] = cpu_move.is_real_word

            if cpu_move.is_game_over:
                if not cpu_move.is_real_word and cpu_move.word is None:
                    # player attempted a word that does not exist
                    ctx['player_lost'] = True
                    ctx['hint'] = game.get_leaf_node(prefix[0:-1])
                elif cpu_move.is_real_word and cpu_move.word is None:
                    # player played a real word
                    ctx['player_lost'] = True
                elif cpu_move.is_real_word and cpu_move.word is not None:
                    # computer played a real word
                    ctx['player_won'] = True

                target_word = cpu_move.word if cpu_move.word is not None else prefix
                target_word = target_word.lower()
                ctx['definition'] = EN_DEFINITIONS.get(target_word, None)

    return render(request, 'game/index.html', ctx)
