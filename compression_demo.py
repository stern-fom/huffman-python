from huffman import HuffmanTree


def demo_compression():
    """Demonstriert die Verwendung der Huffman-Kompression."""

    print("=" * 60)
    print("Huffman-Kompression Demo")
    print("=" * 60 + "\n")

    # Beispiel 1: Direktes compress/decompress
    print("1. Kompression im Speicher")
    print("-" * 40)

    original_data = b"MISSISSIPPI RIVER"
    print(f"Original: {original_data.decode('ascii')}")
    print(f"Groesse: {len(original_data)} Bytes\n")

    # Komprimieren
    tree = HuffmanTree()
    compressed = tree.compress(original_data)

    print(f"Komprimiert: {len(compressed)} Bytes")
    print(f"Header: {compressed[:4].hex()}")
    print(f"Kompressionsrate: {len(compressed) / len(original_data) * 100:.1f}%\n")

    # Dekomprimieren
    decompressed = HuffmanTree.decompress(compressed)
    print(f"Dekomprimiert: {decompressed.decode('ascii')}")
    print(f"Korrekt: {original_data == decompressed}\n")

    # Beispiel 2: Datei-Kompression
    print("\n2. Datei-Kompression")
    print("-" * 40)

    # Komprimieren
    print("Komprimiere 'goethe_faust_i.txt' -> 'goethe_faust_i.huf'...")
    HuffmanTree.compress_file("goethe_faust_i.txt", "goethe_faust_i.huf")
    print()

    # Dekomprimieren
    print("Dekomprimiere 'goethe_faust_i.huf' -> 'goethe_faust_i_dekomprimiert.txt'...")
    HuffmanTree.decompress_file("goethe_faust_i.huf", "goethe_faust_i_dekomprimiert.txt")
    print()

    # Beispiel 3: Binäre Daten
    print("\n3. Binäre Daten")
    print("-" * 40)

    binary_data = bytes([i % 256 for i in range(100)])
    print(f"Original: {len(binary_data)} Bytes")
    print(f"Erste 20 Bytes: {binary_data[:20].hex()}")

    compressed_bin = HuffmanTree().compress(binary_data)
    print(f"\nKomprimiert: {len(compressed_bin)} Bytes")

    decompressed_bin = HuffmanTree.decompress(compressed_bin)
    print(f"Dekomprimiert: {len(decompressed_bin)} Bytes")
    print(f"Identisch: {binary_data == decompressed_bin}\n")

    print("=" * 60)


if __name__ == "__main__":
    demo_compression()
