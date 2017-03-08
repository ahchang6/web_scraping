import networkx as nx
import matplotlib.pyplot as plt
from graph import Graph


graph = Graph()
visual = nx.Graph()
graph.open_json("data/default.json")
color = []

for vertex in graph:
    visual.add_node(vertex.node_id)
    if vertex.is_actor:
        color.append('b')
    else:
        color.append('r')
    for edge in vertex.neighbor:
        visual.add_edge(vertex.node_id, edge)

nx.draw(visual, with_labels=True, node_color=color)
plt.show()
