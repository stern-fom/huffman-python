from huffman import HuffmanTree


def main():
    print("=== Huffman-Baum Demo (Byte-Verarbeitung) ===\n")

    data = b"MISSISSIPPI"
    print(f"Original-Daten: {data}")
    print(f"Als String: {data.decode('ascii')}")
    print(f"Länge: {len(data)} Bytes\n")

    tree = HuffmanTree()
    tree.build_from_bytes(data)

    tree.print_code_table()
    print()

    encoded = tree.encode_bytes(data)
    print(f"Encodierter Bitstring: {encoded}")
    print(f"Länge: {len(encoded)} Bits")
    print(f"Kompressionsrate: {len(encoded) / (len(data) * 8) * 100:.1f}%\n")

    print("=== Einzelnes Byte Encoding ===")
    unique_bytes = sorted(set(data))
    for byte_value in unique_bytes:
        code = tree.encode(byte_value)
        char = chr(byte_value)
        print(f"Byte {byte_value:3d} ('{char}') -> {code}")
    print()

    print("=== Bit-für-Bit Decoding (erste 30 Bits) ===")
    tree.reset_decoder()
    decoded_values = []
    for i, bit in enumerate(encoded[:30]):
        ok, byte_value = tree.decode(bit)
        if ok:
            char = chr(byte_value)
            print(f"Bit {i:2d}: '{bit}' -> Byte gefunden: {byte_value:3d} ('{char}')")
            decoded_values.append(byte_value)
        else:
            print(f"Bit {i:2d}: '{bit}' -> noch kein Byte")

    decoded_data = tree.decode_bytes(encoded)
    print(f"\nDecodierte Daten: {decoded_data}")
    print(f"Als String: {decoded_data.decode('ascii')}")
    print(f"Korrekt: {decoded_data == data}\n")

    print("=== Test mit binären Daten ===")
    binary_data = bytes([0x00, 0xFF, 0x42, 0x42, 0x42, 0x00, 0xFF])
    print(f"Binäre Daten: {binary_data.hex().upper()}")

    tree2 = HuffmanTree()
    tree2.build_from_bytes(binary_data)

    tree2.print_code_table()

    encoded2 = tree2.encode_bytes(binary_data)
    decoded2 = tree2.decode_bytes(encoded2)

    print(f"\nEncodiert: {encoded2}")
    print(f"Decodiert: {decoded2.hex().upper()}")
    print(f"Korrekt: {decoded2 == binary_data}")


if __name__ == "__main__":
    main()
