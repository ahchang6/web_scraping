from bs4 import BeautifulSoup
from graph import Graph
import urllib2
import time
import logging


class Scraper:
    wikipedia = "https://en.wikipedia.org"

    def __init__(self, start_link, cycle, output="data/default.json", in_file=None):
        """
        The constructor class for a Scaper Object
        :param start_link: The link that the crawler will start at
        :param cycle: How many times you want the crawler to cycle
        :param output: the output file of the JSON of the graph
        :param in_file: the input file which can load a graph to continue scraping
        """
        self.start_link = start_link
        self.cycle = cycle
        self.output = output
        self.speed = 2
        self.in_file = in_file

    def set_speed(self, new_speed):
        self.speed = new_speed

    @staticmethod
    def check(soup, graph):
        """
        Checks whether the current page/soup is an actor or film, and returns the node

        :param soup: The soup object passed in that contains the info about current page

        :param graph: The current graph object

        :return: The node created

        """
        bday = soup.find(class_='bday')
        heading = soup.find(id="firstHeading")
        role = soup.find(class_='role')
        film_year = soup.find(class_='bday dtstart published updated')
        year = 0
        is_actor = True
        if role is None:
            is_actor = False
        elif role.string == 'Actor':
            is_actor = True

        print heading.string

        if heading is None:
            return None
        if is_actor and bday is not None:
            year = int(bday.string[:4])
        elif not is_actor:
            if film_year is None:
                year = 0
            else:
                year = int(film_year.string[:4])
        return graph.add_vertex(heading.string, is_actor, year)

    def actor_parser(self, soup, graph, parse_list, node):
        """
        Parses an actor page

        :param soup: The soup object passed in that contains the info about current page

        :param graph: The current graph object

        :param parse_list: The list of things to be parsed in begin()

        :param node: the node that it is working, contains information about the actor
        """
        # checks to see if his filmography is on separate page

        filmography_page = soup.find(title=node.node_id + " filmography")
        if filmography_page is not None:
            # since their filmography page is a wikitable, we can recursively pass it back in
            film_page = urllib2.urlopen(self.wikipedia + filmography_page.get('href'))
            soup = BeautifulSoup(film_page, "html.parser")
            return self.actor_parser(soup, graph, parse_list, node)

        # checks to see if his filmography is a table

        wikitable = soup.find(class_='wikitable sortable')
        if wikitable is not None:
            for row in wikitable.find_all('tr'):
                row = row.find('a')
                if row is None:
                    continue
                print row
                if row.string not in graph.vertex_list.keys():
                    parse_list.append(self.wikipedia + row.get('href'))

        # else, their filmography is probably a list

        else:
            test = soup.find_all('ul')
            for row in test:
                temp = row.find_all('i')
                if len(temp) > 0:
                    for movie in temp:
                        if movie.string not in graph.vertex_list.keys():
                            parse_list.append(self.wikipedia + movie.a.get('href'))
                    return

    def movie_parser(self, soup, graph, parse_list, node):
        """
        Parses an actor page

        :param soup: The soup object passed in that contains the info about current page

        :param graph: The current graph object

        :param parse_list: The list of things to be parsed in begin()

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
                        parse_list.append(self.wikipedia + person.get('href'))
                        weight -= 1
                return

    def begin(self):
        """
        Begins the scraper class with starting link, and crawling all the way until a certain cycle

        :return: The graph created by crawling
        """
        parse_list = []
        graph = Graph()
        if self.in_file is not None:
            graph.open_json(self.in_file)
        start_link = self.start_link
        cycle = self.cycle
        # the loop of parsing
        while start_link is not None and cycle > 0:
            print "Current cycle: " + str(cycle)
            logging.debug("Current cycle: " + str(cycle) + " Current Link: " + str(start_link))
            start_page = urllib2.urlopen(start_link)
            soup = BeautifulSoup(start_page, "html.parser")
            node = self.check(soup, graph)
            # Have yet to parsed _(film) items
            if node is None:
                logging.error("Link: " + str(start_link) + " did not find information")
                start_link = parse_list.pop(0)
                cycle -= 1
                continue
            if node.is_actor:
                self.actor_parser(soup, graph, parse_list, node)
            else:
                self.movie_parser(soup, graph, parse_list, node)
            start_link = parse_list.pop(0)
            time.sleep(self.speed)
            cycle -= 1
        print(str(graph))
        graph.store_json(self.output)
        return graph
