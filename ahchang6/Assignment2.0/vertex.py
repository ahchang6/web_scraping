import json
import string



class Vertex:
    def __init__(self, node_id, is_actor):
        """
        Created a node that is either an actor or film
        :param node_id: Name/identifier of node
        :param is_actor: Whether the node is an actor or not
        """
        self.is_actor = is_actor
        self.node_id = node_id
        self.neighbor = {}

    def __str__(self):
        """
        String form
        :return: (@node_name (Actor/Film): [neighbor one][neighbor two]....[neighbor n])
        """
        node_type = "Film"
        if self.is_actor:
            node_type = "Actor"
        return_string = "(" + str(self.node_id) + node_type + "): "
        for nodeName in self.neighbor.keys():
            if nodeName is None:
                continue
            return_string += "[ " + nodeName + ": " + str(self.neighbor[nodeName]) + "]"
        return return_string

    def add_neighbor(self, neighbor, weight):
        """
        Adds a weighted edge between itself and @neighbor
        :param neighbor: The neightbor to create an edge with
        :param weight: The weight of the edge
        """
        self.neighbor[neighbor] = weight

    def return_neighbor(self):
        """
        Getter for neighbors
        :return: All the neighbors
        """
        return self.neighbor.keys()

    def get_node_id(self):
        """
        Getter for node_id
        :return: The node_id of this object
        """
        return self.node_id

    def is_actor(self):
        """
        Getter for is_actor
        :return: True if self is an actor, False otherwise
        """
        return self.is_actor

    def get_weight(self, neighbor_node_id):
        """
        Getter for the weight of the edge between this and neighbor_node_id
        :param neighbor_node_id: The neighbor you want the edge between
        :return: The weight of the edge
        """

        return self.neighbor[neighbor_node_id]

    def store_json(self):
        """
        Stores this vertex as JSON
        :return: The JSON of this object
        """
        return json.dumps(self.neighbor)

    def open_json(self, in_JSON):
        """
        Restroes the vertex according to JSON
        :param in_JSON: The JSON containing this vertex
        :return: The vertex restored
        """
        self.is_actor = in_JSON['is_actor']
        self.node_id = in_JSON['node_id']
        self.neighbor = in_JSON['neighbor']
        return self

