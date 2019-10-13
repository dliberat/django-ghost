from .Trie import TRIE_BRANCH
from .GhostStrategies import RandomWinBestEffortLossStrat

class GhostMove(object):
    """Describes a move being made by a CPU player.
    In the case where the CPU player has not made
    a move because the previous player's move put the game
    into a completed state, the `word` field is None.
    """
    
    def __init__(self, is_game_over, word, is_real_word=True):
        self.is_game_over = is_game_over
        self.word = word
        self.is_real_word = is_real_word


class GhostGame(object):
    def __init__(self, wordlist):
        """
        Args:
            wordlist (Trie)
        """
        self.wordlist = wordlist
        self.wordlist.calculate_heights()

        self.strategy = RandomWinBestEffortLossStrat()
    

    def make_move(self, current_word):
        """Selects a move to be played next, given the current word.
        
        Args:
            current_word (str) - Current state of the game
        
        Returns:
            None if the current word represents an end state
            (i.e., the opposing player has lost).
            Otherwise, returns a new string representing the
            next word to be played in the game.
        """

        node = self.wordlist.find(current_word)

        # game is finished
        if node is None:
            # word is not reachable from the trie
            # (not a real word or a prefix of a real word)
            return GhostMove(True, None, False)
        elif node.value != TRIE_BRANCH:
            # word is a leaf (it's a real word)
            return GhostMove(True, None, True)
        
        winners = {}
        losers = {}

        # sort the children into winners and losers
        for letter in node.children:
            child = node.children[letter]
            if child.height % 2 == 0:
                losers[letter] = child
            else:
                winners[letter] = child

        suffix = self.strategy.get_move(winners, losers)

        # The strategy provider doesn't tell us which list
        # it got it's selection from, so we have to look it
        # up again to determine whether the game needs to
        # continue or not.
        return self._create_move_obj(current_word, suffix, winners, losers)
    

    def _create_move_obj(self, prefix, suffix, winners, losers):
        word = prefix + suffix

        chosen_node = None

        if suffix in winners:
            chosen_node = winners[suffix]
            is_game_over = chosen_node.height == 0
            
            return GhostMove(is_game_over, word)

        elif suffix in losers:
            chosen_node = losers[suffix]
            is_game_over = chosen_node.height == 0
            return GhostMove(is_game_over, word)

        else:
            # strategy chose a non-real word
            return GhostMove(True, word, False)

            