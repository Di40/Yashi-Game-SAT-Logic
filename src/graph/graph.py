from collections import defaultdict
from src.custom_types import Edge


class Graph:
    def __init__(self, edges=None):
        if edges is None:
            edges = []
        self.adj_list = defaultdict(dict)
        self.edges = set()
        for source_vertex, target_vertex, weight in edges:
            self.add_edge(source_vertex, target_vertex, weight)

    def get_number_of_nodes(self):
        return len(self.adj_list)

    def get_number_of_edges(self):
        return len(self.edges)

    def get_vertices(self):
        return self.adj_list.keys()

    def get_edge_weight(self, source_vertex, target_vertex):
        return self.adj_list[source_vertex].get(target_vertex, None)

    def get_edges(self):
        return self.edges

    def get_neighbors_of_vertex(self, vertex):
        return self.adj_list[vertex].keys()

    def add_edge(self, source_vertex, target_vertex, weight=1):
        self.adj_list[source_vertex][target_vertex] = weight
        self.adj_list[target_vertex][source_vertex] = weight
        edge = Edge((source_vertex, target_vertex, weight))
        reverse_edge = Edge((target_vertex, source_vertex, weight))  # Reverse edge with the same weight
        self.edges.add(edge)
        self.edges.add(reverse_edge)

    def remove_edge(self, source_vertex, target_vertex):
        if target_vertex in self.adj_list[source_vertex]:
            weight = self.adj_list[source_vertex].pop(target_vertex)
            del self.adj_list[target_vertex][source_vertex]
            # del self.adj_list[source_vertex][target_vertex]
            self.edges.remove(Edge((source_vertex, target_vertex, weight)))
            self.edges.remove(Edge((target_vertex, source_vertex, weight)))

    def __xor__(self, other):
        """Find all the edges that are in either the first graph or the second graph, but not in both."""
        return Graph(self.edges.symmetric_difference(other.edges))  # Return the unique edges as a new graph.

    def __eq__(self, other):
        return self.edges == other.edges

    def __hash__(self):
        """Returns the hash of the edges"""
        return hash(frozenset(self.edges))


