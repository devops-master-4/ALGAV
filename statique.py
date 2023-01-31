import time
import random
import string

def random_text(text_length: int) -> str:
     return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(text_length))
     #return ''.join(random.choice(string.ascii_letters) for i in range(text_length))
     #return ''.join(random.choice(string.ascii_letters.lower()) for i in range(text_length))


texte = input('Entrez un texte ou une longueur pour la génération aléatoire : ')
try:
    texte = int(texte)
except:
    texte = str(texte)

if type(texte) == int:
    texte = random_text(texte)
else:
    texte = texte



#start timer
start = time.time()

class Nodes:
    def __init__(self, probability, symbol, gauche=None, droit=None):
        # probabilités des symboles
        self.probability = probability

        # symboles
        self.symbol = symbol

        # le noeud gauche
        self.gauche = gauche

        # le noeud droit
        self.droit = droit

        # la direction de l'arbre (0 gauche, 1 droite)
        self.code = ''


""" Calcul les probabilités de symboles dans les données spécifiées. """
def CalculProba(the_data):
    the_symbols = dict()
    for item in the_data:
        if the_symbols.get(item) == None:
            the_symbols[item] = 1
        else:
            the_symbols[item] += 1
    return the_symbols


""" Affiche les codes des symboles en parcourant l'arbre de Huffman """
the_codes = dict()

def CalculCode(node, value=''):
    #le code huffman pour le noeud courant
    newValue = value + str(node.code)

    if (node.gauche):
        CalculCode(node.gauche, newValue)
    if (node.droit):
        CalculCode(node.droit, newValue)

    if (not node.gauche and not node.droit):
        the_codes[node.symbol] = newValue

    return the_codes


"""résultat encodé"""
def AffichageEncode(the_data, coding):
    encodingOutput = []
    for element in the_data:
        # print(coding[element], end = '')
        encodingOutput.append(coding[element])

    the_string = ''.join([str(item) for item in encodingOutput])
    return the_string


""" Calcule la différence d'espace entre les données compressées et non compressées."""
def TotalGain(the_data, coding):
    # espace total de bits pour stocker les données avant la compression
    avantCompression = len(the_data) * 8
    apresCompression = 0
    the_symbols = coding.keys()
    for symbol in the_symbols:
        the_count = the_data.count(symbol)
        # calculer combien de bits sont nécessaires pour ce symbole au total
        apresCompression += the_count * len(coding[symbol])
    print("Espace utilisé avant compression (en bits):", avantCompression)
    print("Espace utilisé après compression (en bits):", apresCompression)


def HuffmanEncoding(the_data):
    symbolWithProbs = CalculProba(the_data)
    the_symbols = symbolWithProbs.keys()
    the_probabilities = symbolWithProbs.values()
    print("symboles : ", the_symbols)
    print("probabilité : ", the_probabilities)

    the_nodes = []

    # Conversion des symboles et des probabilités en nœuds de l'arbre de Huffman.
    for symbol in the_symbols:
        the_nodes.append(Nodes(symbolWithProbs.get(symbol), symbol))

    while len(the_nodes) > 1:
        # trier tous les noeuds par ordre croissant en fonction de leur probabilité.
        the_nodes = sorted(the_nodes, key=lambda x: x.probability)

        # Sélectionner les deux nœuds les plus petits
        droit = the_nodes[0]
        gauche = the_nodes[1]

        gauche.code = 0
        droit.code = 1

        # Combiner les deux nœuds les plus petits pour créer un nouveau nœud.
        newNode = Nodes(gauche.probability + droit.probability, gauche.symbol + droit.symbol, gauche, droit)

        the_nodes.remove(gauche)
        the_nodes.remove(droit)
        the_nodes.append(newNode)

    huffmanEncoding = CalculCode(the_nodes[0])
    print("symboles avec code", huffmanEncoding)
    TotalGain(the_data, huffmanEncoding)
    encodedOutput = AffichageEncode(the_data, huffmanEncoding)
    return encodedOutput, the_nodes[0]



def HuffmanDecoding(encodedData, huffmanTree):
    treeHead = huffmanTree
    decodedOutput = []
    for x in encodedData:
        if x == '1':
            huffmanTree = huffmanTree.droit
        elif x == '0':
            huffmanTree = huffmanTree.gauche
        try:
            if huffmanTree.gauche.symbol == None and huffmanTree.droit.symbol == None:
                pass
        except AttributeError:
            decodedOutput.append(huffmanTree.symbol)
            huffmanTree = treeHead

    string = ''.join([str(item) for item in decodedOutput])
    return string



#print(texte)
encoding, the_tree = HuffmanEncoding(texte)
print("Encodage affichage : ", encoding)
print("Decodage affichage : ", HuffmanDecoding(encoding, the_tree))
end = time.time()
print("Temps d'exécution total:", end - start, "secondes")
