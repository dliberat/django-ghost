from Trie import TRIE_BRANCH
from GhostStrategies import RandomWinBestEffortLossStrat

class GhostGame(object):
    def __init__(self, wordlist):
        """
        Args:
            wordlist (Trie)
        """
        self.wordlist = wordlist
        self.wordlist.calculate_heights()

        self.strategy = RandomWinBestEffortLossStrat()
    

    def is_game_over(self, word):
        node = self.wordlist.find(word)
        if node is None or node.value != TRIE_BRANCH:
            return True
        return False
    

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

        if node is None or node.value != TRIE_BRANCH:
            # game is finished
            return None
        
        winners = {}
        losers = {}

        # sort the children into winners and losers
        for letter in node.children:
            child = node.children[letter]
            if child.height % 2 == 0:
                losers[letter] = child
            else:
                winners[letter] = child

        move = self.strategy.get_move(winners, losers)
        
        return current_word + move
            