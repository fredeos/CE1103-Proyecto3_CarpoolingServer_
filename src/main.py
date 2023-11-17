from fastapi import FastAPI, HTTPException
from fastapi import Query

import json
from src.dta.Graph import Graph

http_app = FastAPI()

employees = [] # This list saves dictionaries(jsons) of the employees of the app

drivers = [] # This list saves dictionaries(jsons) of the drivers of the app

id_counter = 0 # Variable for counting id

# Grafo con los puntos del mapa
marks = Graph()
    #TODO: Cargar el grafo con una estructura definida
#-------------------------[Generate a default structure for the graph]-------------------------#
with open("src/geodata.txt", "r") as file:
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
            marks.add_connections(data_list)
        else:
            for node in data_list:
                marks.add_new_node(node, None)
        marks.show_nodes()
        marks.show_connections()
#-------------------------[Generate a default structure for the graph]-------------------------#

#-----------------[Reads from the saved files and adds them to the previous lists]-----------------#
with open("src/database/bootup.txt", "r") as file: #Read from the bootup file
    for line in file:
        line = line.strip() # This only removes whitespaces
        strings = line.split(":")

        path = f"src/database/{strings[1][0].upper()}-{strings[0]}.json"
        with open(path, "r") as metadata: # Reads the respective json of the user
            json_file = json.load(metadata)
        
        # Add the JSON object to the respective list
        if strings[1]=="driver":
            drivers.append(json_file)
        if strings[1]=="employee":
            employees.append(json_file)
        
        id_counter += 1

#-----------------[Reads from the saved files and adds them to the previous lists]-----------------#

# >>> Welcome method
@http_app.get("/")
def welcome():
    """
    Welcome message
    """
    return {"message": "Hello World"}

# >>> GET a driver by id
@http_app.get("/drivers/")
def get_driver_by_id(id:int=Query()):
    """
    Looks for a driver based on its id

    Paramters:
        - id(int): id number of the user

    Returns: json object of the user
    """
    for driver in drivers:
        if driver["id"]==id:
            return driver
    
    raise HTTPException(status_code=404, detail="User account not found")

# >>> GET a employee by id
@http_app.get("/employees/")
def get_employee_by_id(id:int=Query()):
    """
    Looks for an employee based on its id

    Paramters:
        - id(int): id number of the user

    Returns: json object of the user
    """
    for employee in employees:
        if employee["id"]==id:
            return employee
    
    raise HTTPException(status_code=404, detail="User account not found")

# >>> Create new user account
# Helper method
def validate_existance(email:str, type:str):
    """
    Verifies if the given user already exists in the system

    Parameters:
        - email(str): emiail of the user
        - type(str): either 'driver' or 'employee' account

    Returns:
        - False if the user hasnt been registered yet or True if the user has already been registered
    """
    if type=="driver":
        for driver in drivers:
            if driver["mail"]==email:
                return True
    if type=="employee":
        for employee in employees:
            if employee["mail"]==email:
                return True
    return False

# Main method
@http_app.post("/accounts/new/")
def create_new_user(name:str=Query(...) , type: str=Query(...) , mail:str=Query(...), password:str=Query(...)):
    """
    Registers an new user in the system as either an employee or a driver. Allows duplication of emails only if
    there is an user with same email as an employee and as a drver.

    Parameters:
        - name(str): username of the user
        - type(str): either a driver or employee classification
        - mail(str): email of the user
        - password(str): security password of the user used upon register

    Returns: 
        - Newly created json object of the user, contains: automatiaclly assigned id, name, email, password, and transportation features
    Exceptions:
        - ERROR 409: Account already exists
    """
    global id_counter
    # Check that the account exists
    if validate_existance(mail, type)==True:
        raise HTTPException(status_code=409, detail="An account is already registered with that email")
    
    # Save the profile information to a dictionary
    id_counter +=1
    user = {
        "id": id_counter,
        "name": name,
        "mail": mail,
        "pass": password,
        "transport?": [False, "None", "None"], # For employees ONLY; is used to know if there is a transport request and from which point to which point
        "available?": [False, "None", "None"], # For drivers ONLY; to save whether the driver is available to transport people or not, and current position and destination
        "traveling": [False, "None"], # Boolean to configure if the travel has already started(for both) and which driver is the transporter(only for users)
        "currentroute": [], # Route the curent user is on
    }

    # Output folder for saving the user json file
    output_path = f"src/database/{type[0].upper()}-{mail}.json"
    # Convert the dict to a jsonstring
    user_string = json.dumps(user)

    # Save the json string to a json file on the database
    with open(output_path, "w") as json_file:
        json_file.write(user_string)
    
    # Update the txt file with the new user
    with open("src/database/bootup.txt", "a") as file:
        file.write("\n")
        file.write(f"{mail}:{type}")

    # Add the newly registered account to the respective list
    if type=="driver":
        drivers.append(user)
    if type=="employee":
        employees.append(user)
    
    return user

# >>> Login to an account(either a Driver or Employee)
@http_app.get("/accounts/login/")
def login_user(name_or_mail:str=Query(...), password:str=Query(...), type:str=Query(...)):
    """
    Retrieves an specified user from the classification based on name or email, and password. Users can either login with their email
    or their name. Depending on which app requests the server, they must use the driver or employee classificatiom.

    Paramters:
        - name_or_mail(str): name or email of the user
        - password(str): password 

    Returns:
        - Json object with the requested credentials
    
    Exceptions:
        - ERROR 404: User was not found or incorrect credentils.
    """
    if type=="driver":
        for driver in drivers:
            if driver["name"]==name_or_mail and driver["pass"]==password:
                return driver
            elif driver["mail"]==name_or_mail and driver["pass"]==password:
                return driver
    if type=="employee":
        for employee in employees:
            if employee["name"]==name_or_mail and employee["pass"]==password:
                return employee
            elif employee["mail"]==name_or_mail and employee["pass"]==password:
                return employee
            
    raise HTTPException(status_code=404, detail="User account not found")
# -----------------------[Graph manipulation]-----------------------#
# >>> Get graph information
@http_app.get("/graph")
def retrieve_graph():
    """
    Retrieves the structure of the graph as json object to share with the client requesting it.

    Returns:
        - Json object of the graph containing the list of nodes with their id, list of people on spot, and list of connections with nodes and weights
    """
    nodes = marks.nodes
    graph_list = []
    json_object = {
        "nodes": []
    }
    for node in nodes:
        graph_list.append({"id": node[0], "connections": marks.get_connections_of_node(node[0]), "users": node[1]})
    json_object["nodes"] = graph_list
    return json_object

# >>> Set the startpoint for a user
@http_app.put("/graph/add:start/user/")
def add_user_startpoint(user_id: int=Query(...), type:str=Query(...), startpoint:str=Query(...)):
    """
    Adds a user to node on the graph as ther startpoint for their travel.

    Parameters:
        - user_id(int): number value of the id
        - type(str): classification of the user as driver or employee
        - startpoint(str): id name of the node of the graph

    Returns:
        - Modified json object of the user witb their transport or availability properties updated for starting a travel

    Exceptions:
        - ERROR 404: User was noyt found
    """
    global marks
    if type.lower()=="driver":
        for driver in drivers:
            if driver["id"]==user_id: # If the user is found then
                driver["available?"][0] = True
                driver["available?"][1] = startpoint.upper()
                marks.add_people_to_node(startpoint, [driver["id"]])
                return driver
    elif type.lower()=="employee":
        for employee in employees:
            if employee["id"]==user_id:
                employee["transport?"][0] = True
                employee["transport?"][1] = startpoint.upper()
                marks.add_people_to_node(startpoint, [employee["id"]])
                return employee
    raise HTTPException(status_code=404, detail=f"User with id({user_id}) was not found in the corresponding user list")
# >>> Set the endpoint for a user
@http_app.put("/graph/add:end/user/")
def add_user_endpoint(user_id: int=Query(...), type:str=Query(...), endpoint:str=Query(...)):
    """
    Adds a user to node on the graph as ther endpoint for their travel.

    Parameters:
        - user_id(int): number value of the id
        - type(str): classification of the user as driver or employee
        - endpoint(str): id name of the node of the graph

    Returns:
        - Modified json object of the user witb their transport or availability properties updated for setting the end of the travel

    Exceptions:
        - ERROR 404: User was noyt found
    """
    global marks
    if type.lower()=="driver":
        for driver in drivers:
            if driver["id"]==user_id: # If the user is found then
                driver["available?"][0] = True
                driver["available?"][2] = endpoint.upper()
                marks.add_people_to_node(endpoint, [driver["id"]])
                return driver
    elif type.lower()=="employee":
        for employee in employees:
            if employee["id"]==user_id:
                employee["transport?"][0] = True
                employee["transport?"][2] = endpoint.upper()
                marks.add_people_to_node(endpoint, [employee["id"]])
                return employee
    raise HTTPException(status_code=404, detail=f"User with id({user_id}) was not found in the corresponding user list")
# >>> Reset the travel parameters of the user and remove from node
@http_app.delete("/graph/rm:endtravel/user/")
def finish_travel(user_id: int=Query(...), type:str=Query(...)):
    """
    On requested from client resets the speciefied user's availability or transport properties back to normal, as
    their travel was either canceled or was finished correctly.

    Parameters;:
        - user_id(int): number value of the id
        - type(str): classification of the user as either driver or employee

    Returns:
        - Modified user json object with its travel properties reset back ti normal

    Exceptions:
        - ERRO 404: User with given id was not found
    """
    global marks
    if type.lower()=="driver":
        for driver in drivers:
            if driver["id"]==user_id:
                driver["available?"][0] = False

                if driver["available?"][1] != "None":
                    marks.remove_people_from_node(driver["available?"][1], [driver["id"]])
                    driver["available?"][1] = "None"

                if driver["available?"][2] != "None":
                    marks.remove_people_from_node(driver["available?"][2], [driver["id"]])
                    driver["available?"][2] = "None"
                return driver
    elif type.lower()=="employee":
        for employee in employees:
            if employee["id"] == user_id:
                employee["transport?"][0] = False

                if employee["transport?"][1] != "None":
                    marks.remove_people_from_node(employee["transport?"][1], [employee["id"]])
                    employee["transport?"][1] = "None"

                if employee["transport?"][2] != "None":
                    marks.remove_people_from_node(employee["transport?"][2], [employee["id"]])
                    employee["transport?"][2] = "None"
                return employee
    raise HTTPException(status_code=404, detail=f"User with id({user_id}) was not found in the corresponding user list")
# >>> TODO: Elegir personas a llevar(solo el conductor) y usar algoritmo de djistra para optimizar la ruta
@http_app.get("/graph/calculate/")
def get_pickup_route(users_to_pickup: list[int]=Query(...), driver_id: int=Query(...)):
    """
    Calculates the appropiate path for the picking up the users selected by the driver and gets the complete route
    to set on the map and the aproximate time to complete the travel.

    Parameters:
        - users_to_pickup(list): contains the ids of the users the driver decided to pickup
        - driver_id(int): id of the driver deciding to start the travel

    Returns:
        - Json object with a list of the complete route of nodes that must be visited and an integer value of the total time.
    """
    # Retrieve the driver doing the pickup
    driver_file = {}
    for driver in drivers:
        if driver["id"]==driver_id:
            driver_file = driver
            break
    # Get starting points of each user in the pickup list
    nodes_to_visit = []
    nodes_to_visit.append(driver_file["available?"][1]) # Add the startpoint of the driver
    for user_id in users_to_pickup:
        for employee in employees:
            if employee["id"] == user_id:
                nodes_to_visit.append(employee["transport?"][1])
    nodes_to_visit.append(driver_file["available?"][2]) # Add the endpoint of the driver
    # Find the route for pair of values in the nodes to visit list
    counter = 0
    all_routes = []
    while counter < len(nodes_to_visit)-1:
        if nodes_to_visit[counter] == nodes_to_visit[counter+1]:
            route = [[nodes_to_visit[counter]], 0]
            all_routes.append(route)
        else:
            route = marks.find_route(nodes_to_visit[counter], nodes_to_visit[counter+1])
            all_routes.append(route)
        counter +=1
    # Once the total path is found: join the routes as one and calculate the total expected time
    final_time = 0
    final_route = []
    for route in all_routes:
        final_time+=route[1]
        for node in route[0]:
            if len(final_route)>0:
                if node != final_route[len(final_route)-1]:
                    final_route.append(node)
            else:
                final_route.append(node)

    return { "route": final_route, "time": final_time}
# -----------------------[Graph manipulation]-----------------------#
# >>> TODO: Agregar y remover puntos al grafo
