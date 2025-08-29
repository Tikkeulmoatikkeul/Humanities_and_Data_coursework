import json
import codecs
import itertools
import networkx as nx
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from utils import cooccurrence

from nltk.tokenize import sent_tokenize
'''
import nltk
nltk.download('punkt')  # 기본적인 punkt 다운로드
nltk.download('punkt_tab')  # punkt_tab 리소스를 다운로드
'''


if __name__ == '__main__':
    # File contains a list of characters, reverse sorted by frequency
    # And a dict with {chapter title: chapter text} key-value pairs
    with codecs.open('hamlet.json', 'r', 'utf-8-sig') as data:
        text = json.load(data)
        cast = text['cast']

        # ##############################################
        # # Build a NetworkX Graph
        # ##############################################
        G = nx.Graph()
        G.name = "The Social Network of Hamlet"
        pairs = cooccurrence(text, cast)
        
        for pair, wgt in pairs.items():
            if wgt>0:
                G.add_edge(pair[0], pair[1], weight=wgt)
        
        # # Make Dorothy the center
        D = nx.ego_graph(G, "Ghost")
        edges, weights = zip(*nx.get_edge_attributes(D, "weight").items())
        
        # # Push nodes away that are less related to Dorothy
        pos = nx.spring_layout(D, k=.5, iterations=40)
        nx.draw(D, pos, node_color="gold", node_size=50, edgelist=edges,
                 width=.5, edge_color="orange", with_labels=True, font_size=12)
        
        plt.savefig("./Hamlet_Social_Network(2129045).png", format="PNG")
        plt.show()