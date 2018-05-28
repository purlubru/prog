import gensim, logging
import networkx as nx
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

m = 'ruscorpora.vec.gz'
model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
model.init_sims(replace=True)
words = ['болеть_VERB', 'жечь_VERB', 'колоть_VERB', 'щипать_VERB', 'гореть_VERB', 'резать_VERB', 'покалывать_VERB', 'тянуть_VERB',
         'дергать_VERB', 'давить_VERB', 'щемить_VERB', 'ломить_VERB']
l = len(words)
G = nx.Graph()
for i in range(l):
    G.add_node(words[i])
for i in range(l):
    for j in range(l):
        if i != j:
            cos = model.similarity(words[i], words[j])
            if cos >= 0.5:
                G.add_edge(words[i], words[j], weight=cos)
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color='blue', node_size=50)
nx.draw_networkx_edges(G, pos, edge_color='green')
nx.draw_networkx_labels(G, pos, font_size=20, font_family='Arial')
plt.axis('off')
plt.show()
deg = nx.degree_centrality(G)
imp = []
for nodeid in sorted(deg, key=deg.get, reverse=True):
    imp.append(nodeid)
f = open('Семантическое поле боли.txt', 'w', encoding='utf8')
f.write('ХАРАКТЕРИСТИКИ ГРАФА\n')
s = imp[0] + ', ' + imp[1] + ', ' + imp[2] + '\n'
f.write('Самые центральные слова графа: ' + s)
s = ''
for comp in list(nx.connected_component_subgraphs(G)):
    s = s + str(nx.radius(comp)) + ' '
f.write('Радиус (для каждой компоненты связности): ' + s + '\n')
f.write('Коэффициент кластеризации: ' + str(nx.average_clustering(G)))
f.close()