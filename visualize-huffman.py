from compare_huffman import load_frequencies
from huffman import HuffmanTree
import graphviz


def visualize_huffman_tree(tree: HuffmanTree, filename: str = "huffman_tree", view: bool = True) -> graphviz.Digraph:
    """
    Visualisiert einen Huffman-Baum mit graphviz.

    Args:
        tree: Der zu visualisierende Huffman-Baum
        filename: Dateiname für die Ausgabe (ohne Erweiterung)
        view: Wenn True, wird die Visualisierung automatisch geöffnet

    Returns:
        graphviz.Digraph Objekt
    """
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

    add_nodes(tree.root)

    dot.render(filename, format='pdf', cleanup=True, view=view)
    print(f"Visualisierung gespeichert als: {filename}.pdf")

    return dot


def main():
    freq = load_frequencies("frequencies.json")
    huffman = HuffmanTree()
    huffman.build_from_frequencies(freq)
    visualize_huffman_tree(huffman)

if __name__ == "__main__":
    main()
