from bs4 import BeautifulSoup
from graph import Graph
from vertex import Vertex
import scrapy


graph = Graph()
b = graph.add_vertex('George Clooney')
b.add_neighbor('a', 20)
a = Vertex('a')
a.add_neighbor('George Clooney', 10)
graph.add_undirected_edge('a', 'George Clooney',20)
soup = BeautifulSoup(r)


