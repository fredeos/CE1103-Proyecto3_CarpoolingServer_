
class Graph:
    """
    Specialized class for holding graphs points of the map, as well as people waiting on any point(node)
    Atributes:
        - nodes(list): holds a tuple or list for the name of the point and a list of users on the point
        - connections(list): holds tuples of the respective connections between two nodes
    """
    nodes = list()
    connections = list()

    def __init__(self):
        self.nodes = []
        self.connections = []
    
    def add_new_node(self, identifier:str, connections:list | None):
        """
        Creates a new node on the graph with or without existing connections if required
        Parameters:
            - identfier(str): Name of the node
            - connection(list): List of names of nodes that are connected to the created node
        """
        node_list = [identifier, []]
        self.nodes.append(node_list)
        if connections!=None:
            # TODO: Logic for arranging the connections based on the names of the connected nodes
            pass

    def set_connection(self, connection_tuple:tuple()):
        """

        """
        self.connections.append(connection_tuple)
