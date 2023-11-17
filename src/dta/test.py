from Graph import Graph

graph = Graph()

graph.add_new_node("S", None)
graph.add_new_node("B", None)
graph.add_new_node("C", None)
graph.add_new_node("D", None)
graph.add_new_node("E", None)
graph.add_new_node("T", None)

graph.add_connections([
    ('S', 'B', 4), ('C', 'S', 2),
    ('B', 'C', 1), ('B', 'D', 5),
    ('C', 'D', 8), ('C', 'E', 10),
    ('D', 'E', 2), ('D', 'T', 6),
    ('E', 'T', 2)                 
                       ])
graph.show_nodes()
graph.show_connections()

graph.find_route("C", "C")
