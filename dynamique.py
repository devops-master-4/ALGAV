import heapq
from collections import defaultdict

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        if other == None:
            return -1
        if not isinstance(other, Node):
            return -1
        return self.freq < other.freq

class HuffmanCoder:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_codes = {}

    def build_huffman_tree(self, text):
        freq_dict = defaultdict(int)
        for char in text:
            freq_dict[char] += 1
        self.heap = [[weight, Node(char, weight)] for char, weight in freq_dict.items()]
        heapq.heapify(self.heap)
        while len(self.heap) > 1:
            lo = heapq.heappop(self.heap)
            hi = heapq.heappop(self.heap)
            node = Node(None, lo[0] + hi[0])
            node.left = lo[1]
            node.right = hi[1]
            heapq.heappush(self.heap, [node.freq, node])
        self.codes = self.generate_huffman_code(self.heap[0][1])
        self.reverse_codes = {v: k for k, v in self.codes.items()}

    def generate_huffman_code(self, node, code=""):
        if not node:
            return {}
        if not node.left and not node.right:
            return {node.char: code}
        return {**self.generate_huffman_code(node.left, code + "0"), **self.generate_huffman_code(node.right, code + "1")}

    def encode(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text

    def decode(self, encoded_text):
        decoded_text = ""
        code = ""
        for bit in encoded_text:
            code += bit
            if code in self.reverse_codes:
                decoded_text += self.reverse_codes[code]
                code = ""
        return decoded_text

hc = HuffmanCoder()
text = "The bird is the word"
hc.build_huffman_tree(text)
encoded_text = hc.encode(text)
decoded_text = hc.decode(encoded_text)
print(f"Text: {text}")
print(f"Encoded text: {encoded_text}")
print(f"Decoded text: {decoded_text}")

# add more text and encode/decode again
text= "Nique sa mère!"
hc.build_huffman_tree(text)
encoded_text = hc.encode(text)
decoded_text = hc.decode(encoded_text)
print(f"Text: {text}")
print(f"Encoded text: {encoded_text}")
print(f"Decoded text: {decoded_text}")
