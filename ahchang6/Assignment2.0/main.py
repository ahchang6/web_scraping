from graph import Graph
from scraper import Scraper
import logging


logging.basicConfig(filename='test.log', level=logging.DEBUG)
test = Scraper('https://en.wikipedia.org/wiki/Ryan_Reynolds', 20)
test.set_speed(1)
graph = test.begin()
print str(graph)

for node in graph:
    if node.is_actor:
        print str(node.node_id) + " is actor"



