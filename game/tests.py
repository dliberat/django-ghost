"""
To run tests from outside of the docker container,
use the following command:

$ docker exec ghost_web_1 python manage.py test

Where `ghost_web_1` is the name of the docker container.
"""

from django.test import TestCase
from unittest.mock import Mock, ANY
import random

from .Trie import Trie, TrieNode, TRIE_BRANCH
from .GhostGame import GhostGame
from .GhostStrategies import GhostStrategy, RandomWinBestEffortLossStrat


class TestGhostGame(TestCase):


    def test_make_move_is_game_over_not_word(self):
        wordlist = Trie()
        wordlist.insert_all(["foo", "bar"])
        game = GhostGame(wordlist)
        zzz = game.make_move("zzz")
        
        assert zzz.is_game_over == True
        assert zzz.word is None


    def test_make_move_is_game_over_is_none(self):
        wordlist = Trie()
        wordlist.insert_all(["foo", "bar"])
        game = GhostGame(wordlist)
        foo = game.make_move("foo")

        assert foo.is_game_over == True
        assert foo.word == None


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

        assert move.word == "bx"
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


    def test_get_leaf_node(self):
        wordlist = Trie()
        wordlist.insert_all(['done', 'douse', 'doberman'])
        game = GhostGame(wordlist)
        leaf = game.get_leaf_node('dob')
        assert leaf == 'doberman'


    def test_get_leaf_node_random(self):
        wordlist = Trie()
        wordlist.insert_all(['done', 'douse', 'doberman'])
        game = GhostGame(wordlist)
        leaf = game.get_leaf_node('do')
        assert leaf in ['done', 'douse', 'doberman']



class TestGhostStratRandomWinBestEffortLoss(TestCase):

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


class TestTrie(TestCase):

    def test_insert_single(self):
        trie = Trie()

        trie.insert("dog")
        
        assert trie.find("dog") is not None

    def test_insert_all(self):
        trie = Trie()
        trie.insert_all(["foo", "bar", "baz"])

        foo = trie.find("foo")
        bar = trie.find("bar")
        baz = trie.find("baz")
        ba = trie.find("ba")

        assert foo.value == "foo"
        assert bar.value == "bar"
        assert baz.value == "baz"
        assert ba.value == TRIE_BRANCH


    def test_insert_branch(self):
        trie = Trie()

        trie.insert("dog")
        trie.insert("dot")

        assert "d" in trie.root.children
        d = trie.root.children["d"]
        assert "o" in d.children
        o = d.children["o"]
        assert "t" in o.children
        assert "g" in o.children
        dot = o.children["t"]
        dog = o.children["g"]

        assert "dot" == dot.value
        assert "dog" == dog.value
    

    def test_find_substring(self):
        trie = Trie()
        trie.insert("foo")

        fo = trie.find("fo")

        assert fo.value == TRIE_BRANCH
    

    def test_find_does_not_exist(self):
        trie = Trie()
        trie.insert("foo")
        trie.insert("bar")
        trie.insert("baz")

        pet = trie.find("pet")
        cpu = trie.find("cpu")

        assert pet is None
        assert cpu is None


    def test_insert_depth(self):
        trie = Trie()
        trie.insert("a")
        trie.insert("aa")
        trie.insert("ab")
        trie.insert("aaa")
        trie.insert("abc")
        trie.insert("ac")

        a = trie.find("a")
        aa = trie.find("aa")
        ab = trie.find("ab")
        aaa = trie.find("aaa")
        abc = trie.find("abc")
        ac = trie.find("ac")

        assert a.depth == 1
        assert aa.depth == 2
        assert ab.depth == 2
        assert aaa.depth == 3
        assert abc.depth == 3
        assert ac.depth == 2
    

    def test_branch_depth(self):
        trie = Trie()
        trie.insert("foobar")
        foo = trie.find("foo")
        assert foo.value == TRIE_BRANCH
        assert foo.depth == 3
    

    def test_heights_single_path(self):
        trie = Trie()
        trie.insert("a")
        trie.insert("aa")
        trie.insert("aaa")

        a = trie.find("a")
        aa = trie.find("aa")
        aaa = trie.find("aaa")

        trie.calculate_heights()

        assert aaa.height == 0
        assert aa.height == 1
        assert a.height == 2


    def test_heights_split_path(self):
        trie = Trie()
        trie.insert("a")
        trie.insert("arwing")
        trie.insert("alabama")
        trie.insert("alimony")

        a = trie.find("a")
        arwing = trie.find("arwing")
        arwin = trie.find("arwin")
        alabama = trie.find("alabama")
        al = trie.find("al")

        trie.calculate_heights()

        assert a.height == 6
        assert al.height == 5
        assert alabama.height == 0
        assert arwing.height == 0
        assert arwin.height == 1

