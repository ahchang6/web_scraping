from unittest import TestCase
from vertex import Vertex


class TestVertex(TestCase):
    def setUp(self):
        self.test_vertex_one = Vertex("test_one", True)
        self.test_vertex_two = Vertex("test_two", False)

    def test_add_neighbor(self):
        self.test_vertex_one.add_neighbor("test_two", 10)
        print str(self.test_vertex_one)
        assert str(self.test_vertex_one) == "test_one (-1/Actor): [ test_two: 10]"
        assert True

    def test_return_neighbor(self):
        self.test_vertex_one.add_neighbor("test_two", 10)
        assert self.test_vertex_one.return_neighbor() == ['test_two']

    def test_get_node_id(self):
        assert self.test_vertex_one.get_node_id() == "test_one"

    def test_get_weight(self):
        self.test_vertex_one.add_neighbor("test_two", 10)
        assert self.test_vertex_one.get_weight("test_two") == 10

