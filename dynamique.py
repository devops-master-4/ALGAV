from collections import defaultdict
import heapq

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

def build_huffman_tree(data:str)-> dict:
    freq = defaultdict(int)
    for char in data:
        freq[char] += 1
    heap = [[weight, char] for char, weight in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

def huffman_encode(data:str)-> dict:
    huff = build_huffman_tree(data)
    encoded_data = {}
    for p in huff:
        encoded_data[p[0]] = p[1]
    return encoded_data

def huffman_decode(data:str,tree: dict)-> str:
    decoded_data = ""
    current = ""
    for char in data:
        current += char
        for key, value in tree.items():
            if value == current:
                decoded_data += key
                current = ""
    return decoded_data

