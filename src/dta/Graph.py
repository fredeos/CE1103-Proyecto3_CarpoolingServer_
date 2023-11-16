
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
    
    # >>> Node manipulation <<<
    def add_new_node(self, identifier:str, connections:list[tuple[str,int]] | None):
        """
        Creates a new node on the graph with or without existing connections if required

        Parameters:
            - identfier(str): Name of the node, preferably an acronym
            - connection(list): List of names of nodes that are connected to the created node 
                                with their respective weight(as tuple(id, weight))
        """
        # Verify the node doesnt already exist
        identifier = identifier.upper() # Changes the identifier to uppercase and it is saved that way
        if self.verify_if_node_in_list(identifier):
            raise Exception("Repeated item on list")
        else:
            node_list = [identifier, []]
            self.nodes.append(node_list) # Adds the new node
            # Adds the respective connections
            if connections!=None:
                for pointB in connections:
                    pointB = (pointB[0].upper(), pointB[1]) # Modifies the tuple list to set the second node upper case
                    if self.verify_if_node_in_list(pointB[0]):
                        if not self.verify_connections(identifier, pointB[0]): # Does a verification
                            self.connections.append((identifier, pointB[0], pointB[1])) # Appends connection(edge) as pointA, pointB, weight
                        else:
                            raise Exception(f"Connection {identifier} with {pointB[0]} already exists")
                    else:
                        raise Exception(f"Node {pointB[0]} doesnt exist in the graph")

    def remove_node(self, node_id:str):
        """
        Removes an existing node of the graph and any related connections to the node

        Parameters:
            - node_id(str): name of the node
        """
        node_id = node_id.upper() # Turns the id into a readable node name for the graph
        if self.verify_if_node_in_list(node_id):
            # 1st remove the node from graph
            for node in self.nodes:
                if node[0] == node_id:
                    self.nodes.remove(node)
            # 2nd remove the connections related to the graph
            newedge = []
            for edge in self.connections:
                if not edge[0]==node_id and not edge[1]==node_id:
                    newedge.append(edge)
            self.connections = newedge
        else:
            raise Exception(f"Node {node_id} doesnt exists in the graph")

    # >>> Node manipulation <<<

    # >>> Edges manipulation <<<
    def add_connections(self, tuple_list:list[tuple[str,str,int]]):
        """
        Adds a list of new connections to the graph WITH a weight distance between the pair.

        Parameters:
            - tuple_list(list): contains a list of tuples representing pairs of connections and 
                                the weight(node_id_A, node_id_B, weight)
        """
        for new_edge in tuple_list:
            new_edge = (new_edge[0].upper(), new_edge[1].upper(), new_edge[2]) # Modifies the connection tuple to an accepted format
            if self.verify_if_node_in_list(new_edge[0]) and self.verify_if_node_in_list(new_edge[1]):
                if not self.verify_connections(new_edge[0], new_edge[1]):
                    self.connections.append(new_edge)
                else:
                    raise Exception(f"Connection {new_edge[0]} with {new_edge[1]} already exists")
            else:
                raise Exception(f"Either node {new_edge[0]} or {new_edge[1]} doesnt exist in the graph")

    def remove_connections(self, tuple_list:list[tuple[str,str]]):
        """
        Removes a list of existing connections on the graph based on the pair that is connected.

        Parameters:
            - tuple_list(list): contains a list of tuples representing pairs of connections and 
                                the weight(node_id_A, node_id_B, weight)
        """
        for rm_edge in tuple_list:
            rm_edge = [rm_edge[0].upper(), rm_edge[1].upper()] # Change the tuple into a readable format for the graph
            if self.verify_if_node_in_list(rm_edge[0]) and self.verify_if_node_in_list(rm_edge[1]):
                for edge in self.connections:
                    # Verify if the connections exist in any way
                    if (edge[0]==rm_edge[0] or edge[0]==rm_edge[1]) and (edge[1]==rm_edge[0] or edge[1]==rm_edge[1]):
                        self.connections.remove(edge)
            else:
                raise Exception(f"Either node {rm_edge[0]} or {rm_edge[1]} doesnt exist on the graph")

    # >>> Edges manipulation <<<
    
    # >>> Auxiliary methods <<<
    def show_nodes(self):
        print(self.nodes)

    def show_connections(self):
        for edge in self.connections:
            print(f"{edge[0]}<-->{edge[1]} : {edge[2]}")

    def verify_if_node_in_list(self, node_id:str):
        """Checks if the given node already exists in the list"""
        for node in self.nodes:
            if node[0]==node_id:
                return True
        return False
    
    def verify_connections(self, nodeA:str, nodeB:str):
        """Checks if the connections between nodes A and B already exists on the list or not"""
        for edge in self.connections:
            if (edge[0]==nodeA or edge[0]==nodeB) and (edge[1]==nodeA or edge[1]==nodeB):
                return True
            
        return False

    def find_route(self, pointA_id, pointB_id): # Implentation of djistra
        """
        Finds the fastest route from point A to point B within the current graph
        """
        pass

    # >>> Auxiliary methods <<<

    # >>> People lists manipulations <<<
    def add_people_to_node(self, node_id:str ,people:list):
        """
        Adds a list of people to the map node with the given id.

        Parameters:
            - node_id(str): name of the node
            - people(list): list of names of people on the node(or mails)

        """
        node_id = node_id.upper()
        if self.verify_if_node_in_list(node_id):
            for node in self.nodes:
                if node[0]==node_id:
                    for person in people:
                        node[1].append(person)
        else:
            raise Exception(f"Node {node_id} doesnt exists in the graph")
    
    def remove_people_from_node(self, node_id:str, people:list[str]):
        """
        Removes a list of people to the map node with the given id.

        Parameters:
            - node_id(str): name of the node
            - people(list): list of names of people on the node(or mails)

        """
        node_id = node_id.upper()
        if self.verify_if_node_in_list(node_id):
            newlist = []
            for node in self.nodes:
                if node[0]==node_id: # Find the node
                    for person in node[1]: # Reconstruct the people list node
                        if person not in people:
                            newlist.append(person)
                    # Set the newlist as the person list of the node
                    node[1] = newlist
        else:
            raise Exception(f"Node {node_id} doesnt exist in the graph")
    
    # >>> People lists manipulations <<<
        
