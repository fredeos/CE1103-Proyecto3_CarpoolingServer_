from Graph import Graph

graph = Graph()

graph.add_new_node("A", None)
graph.add_new_node("B", [("A", 1)])
graph.add_new_node("C", [("B", 7)])
graph.add_new_node("D", [("A", 4)])
graph.add_people_to_node("A", ["Pepe", "Rick"])
graph.add_connections([("A", "C", 10)])

graph.show_nodes()
graph.remove_people_from_node("A", ["Pepe", "Rick"])
graph.show_nodes()
graph.show_connections()

#graph.remove_connections([("C", "b"), ("a", "b")])
graph.remove_connections([("A","C"),("B", "A")])
graph.show_nodes()
graph.show_connections()
