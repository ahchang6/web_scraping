from bs4 import BeautifulSoup
from vertex import Vertex
from graph import Graph
import urllib2
import urllib
import time
import logging


class Scraper:
    def __init__(self, start_link, cycle, output="data/default.json"):
        """
        The constructor class for a Scaper Object
        :param start_link: The link that the crawler will start at
        :param cycle: How many times you want the crawler to cycle
        :param output: the output file of the JSON of the graph
        """
        self.start_link = start_link
        self.cycle = cycle
        self.output = output
        self.speed = 1

    def check(self, soup, graph):
        """
        Checks whether the current page/soup is an actor or film, and returns the node

        :param soup: The soup object passed in that contains the info about current page

        :param graph: The current graph object

        :return: The node created

        """
        bday = soup.find(class_='bday')
        heading = soup.find(id="firstHeading")
        role = soup.find(class_='role')
        is_actor = True
        if role is None:
            is_actor = False
        elif role.string == 'Actor':
            is_actor = True
        print heading.string
        if heading is None:
            return None
        return graph.add_vertex(heading.string, is_actor)

    def actor_parser(self, soup, graph, parse_list):
        """
        Parses an actor page

        :param soup: The soup object passed in that contains the info about current page

        :param graph: The current graph object

        """
        found = False
        wikitable = soup.find(class_='wikitable sortable')
        if wikitable is not None:
            for row in wikitable.find_all('a'):
                if row.string not in graph.vertex_list.keys():
                    parse_list.append("https://en.wikipedia.org" + row.get('href'))

        else:
            test = soup.find_all('ul')
            for row in test:
                temp = row.find_all('i')
                if len(temp) > 0:
                    for movie in temp:
                        if movie.string not in graph.vertex_list.keys():
                            parse_list.append("https://en.wikipedia.org" + movie.a.get('href'))
                    return

    def movie_parser(self, soup, graph, parse_list, node):
        """
        Parses an actor page

        :param soup: The soup object passed in that contains the info about current page

        :param graph: The current graph object

        :param node: The node that is the current movie

        """
        test = soup.find_all('ul')
        for row in test:
            actors = row.find_all('a')
            if len(actors) > 0:
                weight = len(actors)
                for person in actors:
                    if person.string not in graph.vertex_list.keys():
                        graph.add_undirected_edge(person.string, node.node_id, weight)
                        parse_list.append("https://en.wikipedia.org" + person.get('href'))
                        weight -= 1
                return

    def begin(self):
        """
        Begins the scraper class with starting link, and crawling all the way until a certain cycle

        :return: The graph created by crawling
        """
        parse_list = []
        graph = Graph()
        start_link = self.start_link
        cycle = self.cycle
        while start_link is not None:
            print "Current cycle: " + str(cycle)
            logging.debug("Current cycle: " + str(cycle) + " Current Link: " + str(start_link))
            start_page = urllib2.urlopen(start_link)
            soup = BeautifulSoup(start_page, "html.parser")
            node = self.check(soup, graph)
            if node is None:
                logging.error("Link: " + str(start_link) + " did not find information" )
                start_link = parse_list.pop(0)
                cycle -= self.speed
                continue
            if node.is_actor:
                self.actor_parser(soup, graph, parse_list)
            else:
                self.movie_parser(soup, graph, parse_list, node)
            start_link = parse_list.pop(0)
            if cycle < 0:
                break
            time.sleep(2)
            cycle -= self.speed
        graph.store_json(self.output)
        return graph
