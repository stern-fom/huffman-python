import heapq
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
