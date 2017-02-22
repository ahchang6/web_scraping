from vertex import Vertex


class Graph:
    def __init__(self,):
        self.vertex_list = {}
        self.graph_size = 0

    def __iter__(self):
        return iter(self.vertex_list.values())

    def __str__(self):
        return_string = "This graph (size: " + str(self.graph_size) + ") contains: "
        for nodeName in self.vertex_list.values():
            return_string += "[ " + str(nodeName) + " ] "
        return return_string

    def add_vertex(self, node):
        if node in self.vertex_list.keys():
            return None
        self.graph_size += 1

#        if isinstance(node, Vertex):
#           self.vertex_list[node.get_node_id()]=node
#            print "added node"
#            return node
        new_vertex = Vertex(node)
        self.vertex_list[node] = new_vertex
        return new_vertex

    def add_edge(self, source, dest, weight):
        if source not in self.vertex_list.keys():
            self.add_vertex(source)
        if dest not in self.vertex_list.keys():
            self.add_vertex(dest)

        vertex = self.vertex_list[source]
        vertex.add_neighbor(dest, weight)

    def add_undirected_edge(self, node_one, node_two, weight):
        self.add_edge(node_one, node_two, weight)
        self.add_edge(node_two, node_one, weight)


