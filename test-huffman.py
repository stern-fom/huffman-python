from huffman import HuffmanTree
import json

if __name__ == '__main__':
    # Öffne die Textdatei im Binärmodus ("rb") und lese alle Bytes ein.
    # Der Binärmodus ist wichtig, um die exakten Byte-Werte zu erhalten.
    with open("goethe_faust_i.txt", "rb") as f:
        data = f.read()

    # Initialisiere ein leeres Dictionary zur Speicherung der Byte-Häufigkeiten.
    # Schlüssel: Byte-Wert (0-255), Wert: Anzahl des Vorkommens
    freq = {}

    # Iteriere über jeden Byte-Wert in den eingelesenen Daten.
    for byte_value in data:
        # Wenn dieser Byte-Wert noch nicht im Dictionary existiert, initialisiere ihn mit 1.
        if byte_value not in freq:
            freq[byte_value] = 1
        # Ansonsten erhöhe den Zähler um 1.
        else:
            freq[byte_value] += 1

    # Schreibe das Häufigkeits-Dictionary als JSON-Datei.
    # JSON speichert Dictionary-Keys automatisch als Strings, daher werden die Integer-Keys zu Strings konvertiert.
    with open("frequencies.json", "w", encoding="utf-8") as f:
        json.dump(freq, f)

    # Lese die JSON-Datei wieder ein.
    # Das Dictionary freq_str hat nun String-Keys statt Integer-Keys (z.B. "65" statt 65).
    with open("frequencies.json", "r", encoding="utf-8") as f:
        freq_str = json.load(f)

    # Dictionary Comprehension: Erzeuge ein neues Dictionary freq_int mit Integer-Keys.
    # Für jeden Schlüssel in freq_str wird dieser mit int(key) in eine ganze Zahl umgewandelt.
    # Die Werte (Häufigkeiten) bleiben unverändert.
    # Dies ist notwendig, weil JSON alle Keys als Strings speichert, der Huffman-Algorithmus aber Integer-Keys erwartet.
    # Beispiel: {"65": 42} wird zu {65: 42}
    freq_int = {int(key): freq_str[key] for key in freq_str}

    # Erstelle eine neue Instanz des HuffmanTree-Objekts.
    huffman = HuffmanTree()

    # Baue den Huffman-Baum basierend auf den Byte-Häufigkeiten auf.
    # Der Algorithmus erstellt eine optimale Präfix-freie Kodierung für die Datenkompression.
    huffman.build_from_frequencies(freq_int)

    # Gebe die generierte Huffman-Codetabelle aus.
    # Diese zeigt für jeden Byte-Wert die entsprechende binäre Kodierung.
    huffman.print_code_table()

    # Definiere einen Test-String als Bytes.
    # "Keller" wird in seine ASCII-Byte-Werte konvertiert.
    test_bytes = b"Keller"

    # Kodiere die Test-Bytes mit dem Huffman-Algorithmus.
    # Das Ergebnis ist eine komprimierte binäre Darstellung des Strings.
    test_bytes_code = huffman.encode_bytes(test_bytes)

    # Gebe den Original-String und seine Huffman-kodierte Form aus.
    # Dies zeigt die Kompression: Der ursprüngliche String wird in eine kürzere binäre Sequenz umgewandelt.
    print(f"{test_bytes} --> {test_bytes_code}")
