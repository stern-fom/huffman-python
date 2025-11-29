import json

from huffman import HuffmanTree

def load_frequencies(filename: str) -> dict[int, int]:
    with open(filename, "r", encoding="utf-8") as f:
        freq_str = json.load(f)

    return {int(key): freq_str[key] for key in freq_str if freq_str[key] > 0}

if __name__ == '__main__':
    freq_1 = load_frequencies("frequencies.json")
    freq_2 = load_frequencies("faust1_histogram.json")

    huff_1 = HuffmanTree()
    huff_1.build_from_frequencies(freq_1)
    huff_2 = HuffmanTree()
    huff_2.build_from_frequencies(freq_2)

    test_bytes = b"Keller"
    huff_1_code = huff_1.encode_bytes(test_bytes)
    huff_2_code = huff_2.encode_bytes(test_bytes)

    print(huff_1_code)
    print(huff_2_code)
    print("huff_1_code == huff_2_code: {}".format(huff_1_code == huff_2_code))
    print("len(huff_1_code) == len(huff_2_code): {}".format(len(huff_1_code) == len(huff_2_code)))
