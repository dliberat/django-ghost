from abc import ABCMeta, abstractmethod
import random

class GhostStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_move(self, winners, losers):
        """Returns the next letter to be played using the
        current strategy.

        Args:
            winners: dict whose keys are letters and whose
            values are the Trie nodes corresponding to appending
            that letter to the current word. Choosing any of these
            words should lead to a win by the current player
            given optimal play.
            
            losers: dict whose keys are letters and whose values
            are the Trie nodes corresponding to appending that
            letter to the current word. Choosing any of these
            words should lead to a loss by the current player
            given optimal play by the opponent.
        
        Returns:
            A letter to be appended to the end of the current word.
        """
        raise NotImplementedError()


class RandomWinBestEffortLossStrat(GhostStrategy):
    """If the computer thinks it will win, it should play randomly
    among all its winning moves; if the computer thinks it will
    lose, it should play so as to extend the game as long as
    possible (choosing randomly among choices that force the
    maximal game length). 
    """

    def get_move(self, winners, losers):

        if winners:

            return random.choice([letter for letter in winners])

        else:

            # only those nodes that have the longest chain leading to end game state
            max_height = max([x.height for x in losers.values()])
            best_choices = [letter for letter in losers if losers[letter].height == max_height]

            return random.choice(best_choices)


class RandomChoiceStrat(GhostStrategy):
    """Totally random strategy."""

    def get_move(self, winners, losers):
        choices = winners + losers
        return random.choice([letter for letter in choices])