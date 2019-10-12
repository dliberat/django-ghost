from unittest.mock import Mock, ANY

from Trie import Trie, TRIE_BRANCH
from GhostGame import GhostGame


class TestGhostGame:


    def test_is_game_over_full_word(self):
        wordlist = Trie()
        wordlist.insert_all(["foo", "bar"])

        game = GhostGame(wordlist)

        game_over_foo = game.is_game_over("dog")
        game_over_bar = game.is_game_over("bar")

        assert game_over_foo == True
        assert game_over_bar == True


    def test_is_game_over_partial_word(self):
        wordlist = Trie()
        wordlist.insert_all(["foo", "bar", "baz"])
        game = GhostGame(wordlist)
        game_over_ba = game.is_game_over("ba")
        game_over_empty = game.is_game_over("")

        assert game_over_ba == False
        assert game_over_empty == False
    

    def test_is_game_over_impossible_word(self):
        wordlist = Trie()
        wordlist.insert_all(["foo", "bar"])
        game = GhostGame(wordlist)
        game_over_d = game.is_game_over("d")

        assert game_over_d == True


    def test_make_move_is_game_over(self):
        wordlist = Trie()
        wordlist.insert_all(["foo", "bar"])
        game = GhostGame(wordlist)
        foo = game.make_move("foo")
        zzz = game.make_move("zzz")

        assert foo is None
        assert zzz is None


    def test_make_move_use_strat(self):

        class DummyStrat:
            def get_move(self, winners, losers):
                pass
        
        strategy = DummyStrat()
        strategy.get_move = Mock(return_value='x')

        wordlist = Trie()
        wordlist.insert_all(["foo", "bar", "baz"])
        game = GhostGame(wordlist)
        game.strategy = strategy

        move = game.make_move("b")

        assert move == "bx"
        assert strategy.get_move.called


    def test_make_move_provide_winners_losers(self):
        """
                do
            -----------
            |    |    |    
           dog  dot  don       <= LOSERS
                    -----
                      |
                    done       <= WINNER

        """

        class DummyStrat:
            def get_move(self, winners, losers):
                pass
        
        strategy = DummyStrat()
        strategy.get_move = Mock(return_value='x')

        wordlist = Trie()
        wordlist.insert_all(["dog", "dot", "done"])

        game = GhostGame(wordlist)
        game.strategy = strategy
        game.make_move("do")

        # pylint: disable=unpacking-non-sequence
        args, *_ = strategy.get_move.call_args
        winners = args[0]
        losers = args[1]

        assert "g" in losers
        assert "t" in losers
        assert "n" in winners
        assert len(losers) == 2
        assert len(winners) == 1


    def test_make_move_provide_winners_losers_2(self):
        """
                             do
            ---------------------------------
            |    |    |             |       |
           dog  dot  don           dov     doo
                    ------         ---     ---
                    |    |          |       |
                  done  donn       dove    door
                          |
                        donna

        """

        class DummyStrat:
            def get_move(self, winners, losers):
                pass
        
        strategy = DummyStrat()
        strategy.get_move = Mock(return_value='x')

        wordlist = Trie()
        wordlist.insert_all(["dog", "dot", "done", "donna", "dove", "door"])

        game = GhostGame(wordlist)
        game.strategy = strategy
        game.make_move("do")

        # pylint: disable=unpacking-non-sequence
        args, *_ = strategy.get_move.call_args
        winners = args[0]
        losers = args[1]

        assert "g" in losers
        assert "t" in losers
        assert "n" in losers
        assert "v" in winners
        assert "o" in winners
        assert len(losers) == 3
        assert len(winners) == 2
