from Trie import Trie, TRIE_BRANCH

class TestTrie():

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