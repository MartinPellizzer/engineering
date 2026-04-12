import networkx as nx
import matplotlib.pyplot as plt

DG = nx.DiGraph()
# G = nx.DiGraph()
# G = nx.MultiGraph()
# G = nx.MultiDiGraph()

'''
G.add_node('Herbal Medicine')

G.add_node('Herbs')
G.add_node('Phytochemicals')
G.add_node('Conditions')
G.add_node('Preparations')

G.add_node('Infusions')
G.add_node('Decoctions')
G.add_node('Tinctures')
'''

DG.add_edge("Herbal Medicine", "Herbs")
DG.add_edge("Herbal Medicine", "Phytochemicals")
DG.add_edge("Herbal Medicine", "Conditions")
DG.add_edge("Herbal Medicine", "Preparations")
DG.add_edge("Preparations", "Infusions")
DG.add_edge("Preparations", "Decoctions")
DG.add_edge("Preparations", "Tinctures")

print(list(DG.successors('Preparations')))
print(list(DG.predecessors('Preparations')))
# G.add_node(print)

nx.draw_spring(DG, with_labels=True)
plt.show()

