import random

from GhostStrategies import GhostStrategy, RandomWinBestEffortLossStrat
from Trie import TrieNode

random.seed(0)


class TestGhostStratRandomWinBestEffortLoss:

    def test_get_move_winning(self):
        """Given the current word "do", the computer
        should play "don" next, so that the user
        is forced to choose "done"

                do
            -----------
            |    |    |    
           dog  dot  don
                    -----
                      |
                    done  
        """
        g = TrieNode()
        g.height = 0
        t = TrieNode()
        t.height = 0
        n = TrieNode()
        n.height = 1

        winners = {"n": n}
        losers = {"g": g, "t": t}

        strategy = RandomWinBestEffortLossStrat()
        move = strategy.get_move(winners, losers)

        assert move == "n"


    def test_make_move_losing_dont_give_up(self):
        """Given the current word "do", the computer should
        play "don" next, thereby extending the game as
        far as possible.

                do
            -----------
            |    |    |    
           dog  dot  don
                    ------
                    |    |
                  done  donn
                          |
                        donna
        """
        g = TrieNode()
        g.height = 0
        t = TrieNode()
        t.height = 0
        n = TrieNode()
        n.height = 2

        winners = {}
        losers = {"g": g, "t": t, "n": n}

        strategy = RandomWinBestEffortLossStrat()
        move = strategy.get_move(winners, losers)

        assert move == "n"


    def test_make_move_losing_rand_0(self):
        """Select a word at random from a set of losing choices
        all of which have the same height.

                do
            -----------
            |    |    |    
           dog  dot  don
        """

        random.seed(0)

        g = TrieNode()
        g.height = 0
        t = TrieNode()
        t.height = 0
        n = TrieNode()
        n.height = 0

        winners = {}
        losers = {"g": g, "t": t, "n": n}

        strategy = RandomWinBestEffortLossStrat()
        move = strategy.get_move(winners, losers)

        assert move == "t"
    

    def test_make_move_losing_rand_1(self):
        """Select a word at random from a set of losing choices
        all of which have the same height.

                do
            -----------
            |    |    |    
           dog  dot  don
        """

        random.seed(1)

        g = TrieNode()
        g.height = 0
        t = TrieNode()
        t.height = 0
        n = TrieNode()
        n.height = 0

        winners = {}
        losers = {"g": g, "t": t, "n": n}

        strategy = RandomWinBestEffortLossStrat()
        move = strategy.get_move(winners, losers)

        assert move == "g"


    def test_make_move_losing_rand_5(self):
        """Select a word at random from a set of losing choices
        all of which have the same height.

                do
            -----------
            |    |    |    
           dog  dot  don
        """

        random.seed(5)

        g = TrieNode()
        g.height = 0
        t = TrieNode()
        t.height = 0
        n = TrieNode()
        n.height = 0

        winners = {}
        losers = {"g": g, "t": t, "n": n}

        strategy = RandomWinBestEffortLossStrat()
        move = strategy.get_move(winners, losers)

        assert move == "n"


    def test_make_move_winning_rand_0(self):
        """Select a winning move at random from a set
        of winning moves that have varying heights.

                           f
             ----------------------------
             |        |        |        |
            fa       fi       fo       fe
           |   |      |        |        |
          fab  fat   fit      foo      fee
                               |        |
                              foot     feed
                               |
                             footy
        """

        random.seed(0)

        a = TrieNode()
        a.height = 1
        i = TrieNode()
        i.height = 1
        o = TrieNode()
        o.height = 4
        e = TrieNode()
        e.height = 3

        winners = {"a": a, "i": i, "o": o}
        losers = {"e": e}

        strategy = RandomWinBestEffortLossStrat()
        move = strategy.get_move(winners, losers)

        assert move == "i"


    def test_make_move_winning_rand_1(self):
        """Select a winning move at random from a set
        of winning moves that have varying heights.

                           f
             ----------------------------
             |        |        |        |
            fa       fi       fo       fe
           |   |      |        |        |
          fab  fat   fit      foo      fee
                               |        |
                              foot     feed
                               |
                             footy
        """

        random.seed(1)

        a = TrieNode()
        a.height = 1
        i = TrieNode()
        i.height = 1
        o = TrieNode()
        o.height = 4
        e = TrieNode()
        e.height = 3

        winners = {"a": a, "i": i, "o": o}
        losers = {"e": e}

        strategy = RandomWinBestEffortLossStrat()
        move = strategy.get_move(winners, losers)

        assert move == "a"


    def test_make_move_winning_rand_5(self):
        """Select a winning move at random from a set
        of winning moves that have varying heights.

                          f
             ----------------------------
             |        |        |        |
            fa       fi       fo       fe
           |   |      |        |        |
          fab  fat   fit      foo      fee
                               |        |
                              foot     feed
                               |
                             footy
        """

        random.seed(5)

        a = TrieNode()
        a.height = 1
        i = TrieNode()
        i.height = 1
        o = TrieNode()
        o.height = 4
        e = TrieNode()
        e.height = 3

        winners = {"a": a, "i": i, "o": o}
        losers = {"e": e}

        strategy = RandomWinBestEffortLossStrat()
        move = strategy.get_move(winners, losers)

        assert move == "o"


    def test_make_move_winning_nevr_lose(self):
        """Select a winning move at random from a set
        of winning moves that have varying heights.

                          f
             ----------------------------
             |        |        |        |
            fa       fi       fo       fe
           |   |      |        |        |
          fab  fat   fit      foo      fee
                               |        |
                              foot     feed
                               |
                             footy
        """

        a = TrieNode()
        a.height = 1
        i = TrieNode()
        i.height = 1
        o = TrieNode()
        o.height = 4
        e = TrieNode()
        e.height = 3

        winners = {"a": a, "i": i, "o": o}
        losers = {"e": e}

        strategy = RandomWinBestEffortLossStrat()

        for seed in range(5000):
            random.seed(seed)
            move = strategy.get_move(winners, losers)
            assert move != "e"
