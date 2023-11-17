from dta.Graph import Graph

with open("src/geodata.txt", "r") as file:
    graph = Graph()
    for line in file:
        line = line.strip()
        is_tuple = False
        for char in line:
            if char=='-':
                is_tuple = True
        data_list = line.split(":")
        counter = 0
        if is_tuple:
            for tuple in data_list:
                tuple = tuple.split('-')
                data_list[counter] = (tuple[0], tuple[1], int(tuple[2]))
                counter += 1
            graph.add_connections(data_list)
        else:
            for node in data_list:
                graph.add_new_node(node, None)
    graph.show_nodes()
    graph.show_connections()
    print(graph.get_connections_of_node("n2"))