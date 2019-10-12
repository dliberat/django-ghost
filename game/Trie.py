TRIE_BRANCH = -1

class TrieNode(object):
    def __init__(self, depth=0):
        self.value = TRIE_BRANCH
        self.children = dict()
        self.depth = depth
        self.height = -1

class Trie(object):

    def __init__(self, root=None):
        if root is not None:
            self.root = root
        else:
            self.root = TrieNode()
    

    def find(self, value):
        """Searches for a match to the provided value in the trie.
        
        Args:
            value - the value to search for

        Returns:
            - The matched node, if it exists. If the node is a leaf,
            its value will match the provided value. Otherwise,
            its value will be set to TRIE_BRANCH.
            - None if the provided value does not appear in the
            trie and cannot be reached from any node in the trie.
        """
        return self._find(self.root, value)

   
    def insert(self, value):
        """Inserts the provided value into the trie."""
        self._insert(self.root, value)
    

    def insert_all(self, iterable):
        """Inserts the provided values into the trie."""
        for value in iterable:
            self._insert(self.root, value)
    

    def calculate_heights(self):
        """Recalculates heights for all nodes in the tree
        and updates their internal values."""
        self._calculate_heights(self.root)


    def _find(self, node, value):
        for char in value:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node
    

    def _insert(self, node, value):
        for char in value:
            if char not in node.children:
                node.children[char] = TrieNode(node.depth + 1)
            node = node.children[char]
        node.value = value


    def _calculate_heights(self, node):
        if not node.children:
            node.height = 0
            return node.height
        else:
            node.height = max([self._calculate_heights(n) for n in node.children.values()]) + 1
            return node.height
    

    def _debug_print(self, node):
        if not node.children:
            print(node.value)
        else:
            for child in node.children.values():
                self._debug_print(child)

