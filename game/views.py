from django.http import JsonResponse, HttpResponseBadRequest
import re


def validate_word(word):
    return word is not None and re.match(r"^[a-zA-Z]*$", word) is not None


def index(request):

    current_word = request.GET.get('word', None)

    if not validate_word(current_word):
        return HttpResponseBadRequest("Word must be a string of letters.")
    
    current_word = current_word.lower()


    res = dict()
    res['is_game_over'] = False
    res['previous_word'] = current_word
    res['current_word'] = "foo"

    return JsonResponse(res)