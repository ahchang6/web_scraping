from unittest import TestCase
from graph import Graph


class TestGraph(TestCase):
    def setUp(self):
        self.graph = Graph()

    def test_add_vertex(self):
        assert self.graph.graph_size == 0
        self.graph.add_vertex("test_one", True, 1111)
        assert self.graph.graph_size == 1
        assert self.graph.vertex_list.keys() == ["test_one"]

    def test_add_edge(self):
        assert self.graph.graph_size == 0
        self.graph.add_vertex("test_one", True, 1111)
        assert self.graph.graph_size == 1
        self.graph.add_edge("test_one", "test_two", 5)
        assert self.graph.graph_size == 2
        self.graph.add_edge("test_two", "test_one", 3)
        assert self.graph.graph_size == 2
        self.graph.add_edge("test_three", "test_four", 1)
        assert self.graph.graph_size == 4
        assert set(self.graph.vertex_list.keys()) == set(["test_one","test_two","test_three","test_four"])

    def test_add_undirected_edge(self):
        assert self.graph.graph_size == 0
        self.graph.add_vertex("test_one", True, 1111)
        assert self.graph.graph_size == 1
        self.graph.add_undirected_edge("test_one", "test_two", 5)
        assert self.graph.graph_size == 2
        weight_one = self.graph.vertex_list["test_one"].neighbor["test_two"]
        weight_two = self.graph.vertex_list["test_two"].neighbor["test_one"]
        assert weight_one == weight_two

    def test_json(self):
        assert self.graph.graph_size == 0
        self.graph.add_vertex("test_one", True, 1111)
        assert self.graph.graph_size == 1
        self.graph.add_edge("test_one", "test_two", 5)
        assert self.graph.graph_size == 2
        self.graph.add_edge("test_two", "test_one", 3)
        assert self.graph.graph_size == 2
        self.graph.add_edge("test_three", "test_four", 1)
        assert self.graph.graph_size == 4
        self.graph.store_json("test.json")
        graph_two = Graph()
        graph_two.open_json("test.json")
        assert str(self.graph) == str(graph_two)
