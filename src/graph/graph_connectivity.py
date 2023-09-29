def depth_first_search(graph, current_vertex, visited_vertices):
    visited_vertices.add(current_vertex)
    for neighbor_vertex in graph.get_neighbors_of_vertex(current_vertex):
        if neighbor_vertex not in visited_vertices:
            depth_first_search(graph, neighbor_vertex, visited_vertices)


def is_graph_connected(graph):
    visited_vertices = set()
    graph_vertices = graph.get_vertices()
    n_connected = 0
    for start_vertex in graph_vertices:
        if start_vertex not in visited_vertices:
            n_connected += 1
            if n_connected != 1:
                return False
            depth_first_search(graph, start_vertex, visited_vertices)
    return True
