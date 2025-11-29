import heapq
import struct
from typing import Dict, Tuple, Optional


class Node:
    """Repräsentiert einen Knoten im Huffman-Baum."""

    def __init__(self, freq: int, byte_value: Optional[int] = None, left: Optional['Node'] = None, right: Optional['Node'] = None):
        self.freq = freq
        self.byte_value = byte_value
        self.left = left
        self.right = right

    def is_leaf(self) -> bool:
        """Prüft, ob dieser Knoten ein Blatt ist."""
        return self.left is None and self.right is None

    def __lt__(self, other: 'Node') -> bool:
        """Vergleichsoperator für Priority Queue."""
        return self.freq < other.freq


class HuffmanTree:
    """Huffman-Baum mit Encoding- und Decoding-Funktionalität für Bytes."""

    def __init__(self):
        self.root: Optional[Node] = None
        self.code_table: Dict[int, str] = {}
        self.current_node: Optional[Node] = None

    def build_from_frequencies(self, freq_dict: Dict[int, int]) -> None:
        """
        Baut den Huffman-Baum aus einem Häufigkeiten-Dictionary auf.

        Args:
            freq_dict: Dictionary mit Byte-Werten (0-255) als Keys und Häufigkeiten als Values
        """
        if not freq_dict:
            raise ValueError("Häufigkeiten-Dictionary darf nicht leer sein")

        if len(freq_dict) == 1:
            byte_value = list(freq_dict.keys())[0]
            freq = freq_dict[byte_value]
            self.root = Node(freq, byte_value)
            self.code_table = {byte_value: "0"}
            self.current_node = self.root
            return

        priority_queue = [Node(freq, byte_value) for byte_value, freq in freq_dict.items()]
        heapq.heapify(priority_queue)

        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            if right.freq < left.freq:
                left, right = right, left

            parent = Node(left.freq + right.freq, left=left, right=right)
            heapq.heappush(priority_queue, parent)

        self.root = priority_queue[0]
        self.current_node = self.root
        self._build_code_table()

    def build_from_bytes(self, data: bytes) -> None:
        """
        Berechnet Häufigkeiten aus Byte-Daten und baut den Baum auf.

        Args:
            data: Byte-Daten, aus denen die Häufigkeiten berechnet werden
        """
        if not data:
            raise ValueError("Byte-Daten dürfen nicht leer sein")

        freq_dict = {}
        for byte_value in data:
            freq_dict[byte_value] = freq_dict.get(byte_value, 0) + 1

        self.build_from_frequencies(freq_dict)

    def _build_code_table(self) -> None:
        """Erstellt die Code-Tabelle durch Baum-Traversierung."""
        self.code_table = {}

        def traverse(node: Optional[Node], code: str) -> None:
            if node is None:
                return

            if node.is_leaf():
                self.code_table[node.byte_value] = code if code else "0"
            else:
                traverse(node.left, code + "0")
                traverse(node.right, code + "1")

        traverse(self.root, "")

    def encode(self, byte_value: int) -> str:
        """
        Encodiert ein Byte zu einem Bitstring.

        Args:
            byte_value: Zu encodierendes Byte (0-255)

        Returns:
            Bitstring als String (z.B. "1011")

        Raises:
            ValueError: Wenn das Byte nicht im Baum vorhanden ist
        """
        if byte_value not in self.code_table:
            raise ValueError(f"Byte {byte_value} ist nicht im Huffman-Baum enthalten")

        return self.code_table[byte_value]

    def encode_bytes(self, data: bytes) -> str:
        """
        Encodiert Byte-Daten zu einem Bitstring.

        Args:
            data: Zu encodierende Byte-Daten

        Returns:
            Bitstring als String
        """
        return ''.join(self.encode(byte_value) for byte_value in data)

    def decode(self, bit: str) -> Tuple[bool, Optional[int]]:
        """
        Decodiert ein einzelnes Bit. Stateful - wandert durch den Baum.

        Args:
            bit: Ein einzelnes Bit als String ('0' oder '1')

        Returns:
            Tupel (ok, byte_value):
            - ok=False, byte_value=None: Noch kein Blatt erreicht
            - ok=True, byte_value=Byte-Wert: Blatt erreicht, Decoder wurde zurückgesetzt

        Raises:
            ValueError: Wenn bit nicht '0' oder '1' ist oder Baum nicht initialisiert
        """
        if bit not in ('0', '1'):
            raise ValueError(f"Bit muss '0' oder '1' sein, erhalten: '{bit}'")

        if self.root is None:
            raise ValueError("Baum ist nicht initialisiert")

        if self.current_node is None:
            self.current_node = self.root

        if self.root.is_leaf():
            byte_value = self.root.byte_value
            return (True, byte_value)

        if bit == '0':
            self.current_node = self.current_node.left
        else:
            self.current_node = self.current_node.right

        if self.current_node.is_leaf():
            byte_value = self.current_node.byte_value
            self.current_node = self.root
            return (True, byte_value)

        return (False, None)

    def decode_bytes(self, bitstring: str) -> bytes:
        """
        Decodiert einen Bitstring zu Byte-Daten.

        Args:
            bitstring: Bitstring als String (z.B. "10110011")

        Returns:
            Decodierte Byte-Daten
        """
        self.reset_decoder()
        result = []

        for bit in bitstring:
            ok, byte_value = self.decode(bit)
            if ok:
                result.append(byte_value)

        return bytes(result)

    def reset_decoder(self) -> None:
        """Setzt den Decoder-Zustand zurück zur Wurzel."""
        self.current_node = self.root

    def get_code_table(self) -> Dict[int, str]:
        """
        Gibt die Code-Tabelle zurück.

        Returns:
            Dictionary mit Byte-Werten als Keys und Bitstrings als Values
        """
        return self.code_table.copy()

    def print_code_table(self) -> None:
        """Gibt die Code-Tabelle formatiert aus."""
        print("Huffman-Code-Tabelle:")
        print("-" * 40)
        for byte_value, code in sorted(self.code_table.items()):
            char = chr(byte_value) if 32 <= byte_value <= 126 else '?'
            print(f"Byte {byte_value:3d} ('{char}') -> {code}")

    def visualize(self, filename: str = "huffman_tree", view: bool = False):
        """
        Visualisiert den Huffman-Baum mit graphviz.

        Args:
            filename: Dateiname für die Ausgabe (ohne Erweiterung)
            view: Wenn True, wird die Visualisierung automatisch geöffnet

        Returns:
            graphviz.Digraph Objekt (oder None, wenn graphviz nicht installiert ist)
        """
        try:
            import graphviz
        except ImportError:
            print("Fehler: graphviz-Modul nicht installiert.")
            print("Installieren Sie es mit: pip install graphviz")
            return None

        dot = graphviz.Digraph(comment='Huffman Tree')
        dot.attr(rankdir='TB')
        dot.attr('node', shape='circle', style='filled')

        node_counter = [0]

        def add_nodes(node, parent_id=None, edge_label=None):
            if node is None:
                return

            current_id = f"node_{node_counter[0]}"
            node_counter[0] += 1

            if node.is_leaf():
                char = chr(node.byte_value) if 32 <= node.byte_value <= 126 else '?'
                label = f"Byte: {node.byte_value}\n'{char}'\nFreq: {node.freq}"
                dot.node(current_id, label, fillcolor='lightblue')
            else:
                label = f"Freq: {node.freq}"
                dot.node(current_id, label, fillcolor='lightgray')

            if parent_id is not None:
                dot.edge(parent_id, current_id, label=edge_label)

            if not node.is_leaf():
                add_nodes(node.left, current_id, '0')
                add_nodes(node.right, current_id, '1')

        add_nodes(self.root)

        dot.render(filename, format='pdf', cleanup=True, view=view)
        print(f"Visualisierung gespeichert als: {filename}.pdf")

        return dot

    def _serialize_tree(self) -> str:
        """
        Serialisiert den Baum als Bitstring (Pre-Order Traversierung).

        Format:
        - Innerer Knoten: '0' + rekursiv left + right
        - Blattknoten: '1' + 8-Bit Byte-Wert

        Returns:
            Bitstring-Repräsentation des Baums
        """
        def serialize_node(node: Optional[Node]) -> str:
            if node is None:
                return ''

            if node.is_leaf():
                # '1' + 8 Bit für Byte-Wert
                return '1' + format(node.byte_value, '08b')
            else:
                # '0' + rekursiv left und right
                return '0' + serialize_node(node.left) + serialize_node(node.right)

        return serialize_node(self.root)

    def _deserialize_tree(self, bitstring: str, pos: int = 0) -> Tuple[Optional[Node], int]:
        """
        Deserialisiert einen Baum aus einem Bitstring.

        Args:
            bitstring: Serialisierter Baum als Bitstring
            pos: Aktuelle Position im Bitstring

        Returns:
            Tupel (Node, neue_position)
        """
        if pos >= len(bitstring):
            return None, pos

        if bitstring[pos] == '1':
            # Blattknoten: nächste 8 Bits sind der Byte-Wert
            byte_value = int(bitstring[pos+1:pos+9], 2)
            return Node(0, byte_value), pos + 9
        else:
            # Innerer Knoten: '0' + left + right
            left, pos = self._deserialize_tree(bitstring, pos + 1)
            right, pos = self._deserialize_tree(bitstring, pos)
            return Node(0, left=left, right=right), pos

    @staticmethod
    def _bitstring_to_bytes(bitstring: str) -> bytes:
        """
        Konvertiert einen Bitstring in Bytes (mit Padding).

        Args:
            bitstring: String aus '0' und '1'

        Returns:
            Bytes-Repräsentation
        """
        # Padding auf nächstes 8er-Vielfaches
        padding = (8 - len(bitstring) % 8) % 8
        bitstring_padded = bitstring + '0' * padding

        # In 8er-Gruppen aufteilen und zu Bytes konvertieren
        byte_array = []
        for i in range(0, len(bitstring_padded), 8):
            byte = int(bitstring_padded[i:i+8], 2)
            byte_array.append(byte)

        return bytes(byte_array)

    @staticmethod
    def _bytes_to_bitstring(data: bytes, num_bits: int) -> str:
        """
        Konvertiert Bytes in einen Bitstring mit gegebener Länge.

        Args:
            data: Byte-Daten
            num_bits: Anzahl gültiger Bits

        Returns:
            Bitstring
        """
        bitstring = ''.join(format(byte, '08b') for byte in data)
        return bitstring[:num_bits]

    def compress(self, data: bytes) -> bytes:
        """
        Komprimiert Byte-Daten mit Huffman-Codierung.

        Format:
        [HEADER: 4 bytes] - "HUF\x01"
        [TREE_SIZE: 4 bytes] - Länge der Baum-Daten (uint32, big-endian)
        [TREE_DATA: variable] - Serialisierter Baum
        [DATA_BITS: 4 bytes] - Anzahl gültiger Bits (uint32, big-endian)
        [DATA: variable] - Codierte Daten

        Args:
            data: Zu komprimierende Byte-Daten

        Returns:
            Komprimierte Daten als Bytes
        """
        if not data:
            raise ValueError("Daten dürfen nicht leer sein")

        # Baum erstellen
        self.build_from_bytes(data)

        # Daten encodieren
        encoded_bitstring = self.encode_bytes(data)

        # Baum serialisieren
        tree_bitstring = self._serialize_tree()
        tree_bytes = self._bitstring_to_bytes(tree_bitstring)

        # Codierte Daten zu Bytes konvertieren
        data_bytes = self._bitstring_to_bytes(encoded_bitstring)

        # Header zusammenbauen
        header = b'HUF\x01'
        tree_size = struct.pack('>I', len(tree_bytes))
        data_bits = struct.pack('>I', len(encoded_bitstring))

        return header + tree_size + tree_bytes + data_bits + data_bytes

    @staticmethod
    def decompress(compressed_data: bytes) -> bytes:
        """
        Dekomprimiert Huffman-codierte Daten.

        Args:
            compressed_data: Komprimierte Daten

        Returns:
            Dekomprimierte Byte-Daten
        """
        if len(compressed_data) < 16:
            raise ValueError("Ungültige komprimierte Daten (zu kurz)")

        # Header validieren
        header = compressed_data[0:4]
        if header != b'HUF\x01':
            raise ValueError(f"Ungültiger Header: {header}")

        # Baum-Größe lesen
        tree_size = struct.unpack('>I', compressed_data[4:8])[0]

        # Baum-Daten extrahieren
        tree_end = 8 + tree_size
        if tree_end > len(compressed_data):
            raise ValueError("Ungültige Baum-Größe")

        tree_bytes = compressed_data[8:tree_end]

        # Daten-Bits-Länge lesen
        data_bits = struct.unpack('>I', compressed_data[tree_end:tree_end+4])[0]

        # Codierte Daten extrahieren
        data_bytes = compressed_data[tree_end+4:]

        # Baum deserialisieren
        tree_bitstring = HuffmanTree._bytes_to_bitstring(tree_bytes, len(tree_bytes) * 8)
        tree = HuffmanTree()
        tree.root, _ = tree._deserialize_tree(tree_bitstring)
        tree.current_node = tree.root
        tree._build_code_table()

        # Daten decodieren
        data_bitstring = HuffmanTree._bytes_to_bitstring(data_bytes, data_bits)
        decoded_data = tree.decode_bytes(data_bitstring)

        return decoded_data

    @staticmethod
    def compress_file(input_file: str, output_file: str) -> None:
        """
        Komprimiert eine Datei.

        Args:
            input_file: Pfad zur Eingabedatei
            output_file: Pfad zur Ausgabedatei
        """
        with open(input_file, 'rb') as f:
            data = f.read()

        tree = HuffmanTree()
        compressed = tree.compress(data)

        with open(output_file, 'wb') as f:
            f.write(compressed)

        print(f"Komprimiert: {len(data)} -> {len(compressed)} Bytes")
        print(f"Kompressionsrate: {len(compressed) / len(data) * 100:.2f}%")

    @staticmethod
    def decompress_file(input_file: str, output_file: str) -> None:
        """
        Dekomprimiert eine Datei.

        Args:
            input_file: Pfad zur komprimierten Datei
            output_file: Pfad zur Ausgabedatei
        """
        with open(input_file, 'rb') as f:
            compressed = f.read()

        decompressed = HuffmanTree.decompress(compressed)

        with open(output_file, 'wb') as f:
            f.write(decompressed)

        print(f"Dekomprimiert: {len(compressed)} -> {len(decompressed)} Bytes")
