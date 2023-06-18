class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class Dictionary:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_word = True

    def search(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_word

    def starts_with(self, prefix):
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]
        words = []
        self._collect_words(current, prefix, words)
        return words

    def _collect_words(self, node, prefix, words):
        if node.is_word:
            words.append(prefix)
        for char, child_node in node.children.items():
            self._collect_words(child_node, prefix + char, words)

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if node is None:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert_recursive(node.left, key)
        else:
            node.right = self._insert_recursive(node.right, key)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance_factor = self._get_balance_factor(node)

        if balance_factor > 1:
            if key < node.left.key:
                return self._rotate_right(node)
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

        if balance_factor < -1:
            if key > node.right.key:
                return self._rotate_left(node)
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        return node

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _get_height(self, node):
        if node is None:
            return 0
        return node.height

    def _get_balance_factor(self, node):
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def inorder_traversal(self):
        result = []
        self._inorder_traversal_recursive(self.root, result)
        return result

    def _inorder_traversal_recursive(self, node, result):
        if node:
            self._inorder_traversal_recursive(node.left, result)
            result.append(node.key)
            self._inorder_traversal_recursive(node.right, result)

class DictionaryWithTrieAndAVL:
    def __init__(self):
        self.trie = Dictionary()
        self.avl_tree = AVLTree()

    def insert(self, word):
        self.trie.insert(word)
        self.avl_tree.insert(word)

    def search(self, word):
        return self.trie.search(word)

    def starts_with(self, prefix):
        return self.trie.starts_with(prefix)

    def sorted_words(self):
        return self.avl_tree.inorder_traversal()

# Example usage:
dictionary = DictionaryWithTrieAndAVL()

file_path = r'C:\Users\user\Desktop\academics\sem3\python programs'
# Read words from file
with open('word1.txt', 'r') as file:
    words = file.read().split()

# Insert words into the dictionary
for word in words:
    dictionary.insert(word)

# Prompt user for word to search
word_to_search = input("Enter a word to search: ")
found = dictionary.search(word_to_search)
if found:
    print("Word found!")
else:
    print("Word not found!")

# Prompt user for prefix to search
prefix_to_search = input("Enter a prefix to search: ")
words_with_prefix = dictionary.starts_with(prefix_to_search)
print("Words starting with '{}': {}".format(prefix_to_search, words_with_prefix))

# Get all words in sorted order
sorted_words = dictionary.sorted_words()
print("Sorted words:", sorted_words)
