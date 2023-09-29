from pysat.formula import WCNF
from collections import deque, defaultdict
from src.graph.graph import Graph
from src.utils import powerset


def init_graph(lines):
    g = Graph()
    for edge in lines.values():
        g.add_edge(*edge)
    return g


def find_path_in_graph(graph, start_vertex, end_vertex, parents_map):
    """Finds a path from start_vertex to end_vertex in the given graph and returns it as a subgraph."""
    path_subgraph = Graph()
    current_vertex = end_vertex
    while current_vertex is not None and current_vertex != start_vertex:
        parent_vertex = parents_map[current_vertex]
        edge_weight = graph.get_edge_weight(current_vertex, parent_vertex)
        path_subgraph.add_edge(current_vertex, parent_vertex, edge_weight)
        current_vertex = parent_vertex
    return path_subgraph


def get_fundamental_cycles(graph, root_vertex):
    in_tree = defaultdict(bool)  # A dict that keeps track of whether a vertex u is in the spanning_tree.
    # It is initially set to False for all vertices.
    spanning_tree = Graph()  # It starts empty and will gradually grow during the execution of the algorithm.
    queue = deque([root_vertex])  # double-ended queue
    parent_vertices = defaultdict(lambda: None)  # A dict that will store the parent-child relationships in the tree.
    # It is initialized with all vertices having no parent (None).
    fundamental_cycles = set()

    while queue:  # Depth-first search (DFS)
        # We start with the root_vertex and explore its neighbors one by one.
        current_vertex = queue.popleft()
        for neighbor_vertex in graph.get_neighbors_of_vertex(current_vertex):
            if neighbor_vertex != parent_vertices[current_vertex]:  # To avoid revisiting the parent.
                # This condition ensures that we do not revisit the vertex we came from, avoiding backtracking.
                if in_tree[neighbor_vertex]:  # If neighbor_vertex is in the spanning_tree a fundamental cycle is found.
                    path_from_root_to_current = find_path_in_graph(spanning_tree, root_vertex,
                                                                   current_vertex, parent_vertices)
                    path_from_root_to_neighbor = find_path_in_graph(spanning_tree, root_vertex,
                                                                    neighbor_vertex, parent_vertices)
                    # Combine paths using XOR and add edge between then to create a cycle.
                    cycle = path_from_root_to_neighbor ^ path_from_root_to_current  # XOR
                    cycle.add_edge(neighbor_vertex, current_vertex,
                                   graph.get_edge_weight(neighbor_vertex, current_vertex))
                    fundamental_cycles.add(cycle)
                else:  # neighbor_vertex is not in the tree => It's an unvisited neighbor.
                    queue.append(neighbor_vertex)
                    in_tree[neighbor_vertex] = True  # Mark neighbor_vertex as visited and in the tree.
                    spanning_tree.add_edge(current_vertex, neighbor_vertex,  # Add new edge to the spanning tree.
                                           graph.get_edge_weight(current_vertex, neighbor_vertex))
                    parent_vertices[neighbor_vertex] = current_vertex  # current_vertex <- parent of neighbor_vertex.

    return fundamental_cycles


def find_all_cycles(graph):
    """Finds all cycles in a given graph using a combination of fundamental cycles."""
    root_vertex = next(iter(graph.get_vertices()), None)
    fundamental_cycles = get_fundamental_cycles(graph, root_vertex)
    all_cycles  = []

    for cycle_combination in powerset(fundamental_cycles):  # All possible combinations of fundamental cycles.
        if cycle_combination:
            new_cycle = Graph()
            for cycle in cycle_combination:  # Individual cycles
                new_cycle ^= cycle  # Use XOR to merge cycles.
            all_cycles.append(new_cycle.get_edges())

    return all_cycles


def calculate_no_cycles_constraint(graph, points_to_lines):
    all_cycles = find_all_cycles(graph)

    phi_no_cycles = WCNF()
    for cycle in all_cycles:
        clause = [-points_to_lines[start_vertex][end_vertex] for start_vertex, end_vertex, _ in cycle]
        if clause:
            phi_no_cycles.append(clause)

    return phi_no_cycles
