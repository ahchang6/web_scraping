from vertex import Vertex
import logging
import json


class Graph:
    def __init__(self):
        """
        Constructor for a Graph Object
        """
        self.vertex_list = {}
        self.graph_size = 0

    def __iter__(self):
        """
        Iterator
        :return: Returns the iterative of the values of the vertex list
        """
        return iter(self.vertex_list.values())

    def __str__(self):
        """
        When passed through, will read:
        "This graph (size: @size) contains: [node_one][node_two]....][node_n]
        :return: The string parsed
        """
        return_string = "This graph (size: " + str(self.graph_size) + ") contains: "
        for nodeName in self.vertex_list.values():
            if nodeName is None:
                continue
            return_string += "[ " + str(nodeName) + " ] "
        return return_string

    def add_vertex(self, node, is_actor, year):
        """
        Adds a vertex with the node_id of node
        :param node: The node_id/header
        :param is_actor: If node is an actor
        :param year: Year or film or actor
        :return: The added vertex
        """
        logging.info("Adding vertex: " + str(node))
        if node in self.vertex_list.keys():
            if self.vertex_list[node].year == 0 and year != 0:
                self.vertex_list[node].year = year
            else:
                return None

        self.graph_size += 1

        new_vertex = Vertex(node, is_actor, year)
        if new_vertex is None:
            return None

        self.vertex_list[node] = new_vertex
        return new_vertex

    def add_edge(self, source, dest, weight):
        """
        Adds a weighted directed edge from source to dest
        :param source: Where the directed edge starts
        :param dest: Where the directed edge ends
        :param weight: The weight of the directed edge
        """
        if source not in self.vertex_list.keys():
            self.add_vertex(source, True, 0)
        if dest not in self.vertex_list.keys():
            self.add_vertex(dest, True, 0)
        vertex = self.vertex_list[source]
        vertex.add_neighbor(dest, weight)

    def add_undirected_edge(self, node_one, node_two, weight):
        """
        Adds a weighted undirected edge between node_one and node_two
        :param node_one: Endpoint of an undirected edge
        :param node_two: Endpoint of an undirected edge
        :param weight: The weight of the undirected edge
        """
        self.add_edge(node_one, node_two, weight)
        self.add_edge(node_two, node_one, weight)

    def store_json(self, outfile_name):
        """
        Stores the graph as a JSON
        :param outfile_name: The file where the JSON will be stored
        """

        json_item = json.dumps(self, default=lambda o: o.__dict__)
        with open(outfile_name, 'w') as outfile:
            outfile.write(json_item)

    def open_json(self, infile):
        """
        Restores a graph through a JSON file
        :param infile: The file where the graph is stored
        :return: The graph restored
        """
        json_data = open(infile).read()
        #sets data
        parsed_dict = json.loads(json_data)
        self.graph_size=parsed_dict['graph_size']
        parsed_dict = parsed_dict['vertex_list']
        for key in parsed_dict.keys():
            vertex = Vertex(key, False, 0000)
            self.vertex_list[key] = vertex.open_json(parsed_dict[key])
        return self



