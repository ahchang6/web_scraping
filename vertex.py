class Vertex:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbor = {}

    def __str__(self):
        return_string = str(self.node_id) + ": "
        for nodeName in self.neighbor.keys():
            return_string += "[ " + nodeName + ": " + str(self.neighbor[nodeName]) + "]"
        return return_string

    def add_neighbor(self, neighbor, weight):
        self.neighbor[neighbor] = weight

    def return_neighbor(self):
        return self.neighbor.keys()

    def get_node_id(self):
        return self.node_id

    def get_weight(self, neighbor_node_id):
        return self.neighbor[neighbor_node_id]
