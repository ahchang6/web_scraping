from bs4 import BeautifulSoup
from graph import Graph
from vertex import Vertex
from actor_spider import ActorSpider
import scrapy
import logging
from scraper import Scraper


logging.basicConfig(filename='test.log', level=logging.DEBUG)




test = Scraper('https://en.wikipedia.org/wiki/Morgan_Freeman')
graph = test.begin()
print str(graph)
graph_two = Graph()
graph_two.open_json('data/test.json')
print str(graph_two)



