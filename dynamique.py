import heapq
from collections import defaultdict
import string

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

        for char in string.printable:
            freq_dict[char] += 0

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
    
    def update_tree(self, char):
        node_found = False
        for i in range(len(self.heap)):
            node = self.heap[i][1]
            if node.char == char:
                node_found = True
                node.freq += 1
                self.heap[i][0] = node.freq
                break
        if not node_found:
            node = Node(char, 1)
            self.heap.append([1, node])
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

# execute the program
if __name__ == "__main__":
    huffman_coder = HuffmanCoder()
    text = "abracadabra"
    huffman_coder.build_huffman_tree(text)
    encoded_text = huffman_coder.encode(text)
    print(encoded_text)
    decoded_text = huffman_coder.decode(encoded_text)
    print(decoded_text)
    huffman_coder.update_tree('H')
    encoded_text = huffman_coder.encode(text)
    print(encoded_text)
    decoded_text = huffman_coder.decode(encoded_text)
    print(decoded_text)
