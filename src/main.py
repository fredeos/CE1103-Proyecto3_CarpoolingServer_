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
    return {"message": "Hello World"}

# >>> GET a driver by id
@http_app.get("/drivers/")
def get_driver_by_id(id:int=Query()):
    for driver in drivers:
        if driver["id"]==id:
            return driver
    
    raise HTTPException(status_code=404, detail="User account not found")

# >>> GET a employee by id
@http_app.get("/employees/")
def get_employee_by_id(id:int=Query()):
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
    # Check that the account exists
    if validate_existance(mail, type)==True:
        raise HTTPException(status_code=409, detail="An account is already registered with that email")
    
    # Save the profile information to a dictionary
    user = {
        "id": id_counter+1,
        "name": name,
        "mail": mail,
        "pass": password,
        "transport?": [False, "None", "None"], # For employees ONLY; is used to know if there is a transport request and from which point to which point
        "availabe?": [False, "None", "None"], # For drivers ONLY; to save whether the driver is available to transport people or not, and current position and destination
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

# >>> TODO: Agregar y remover puntos al grafo
# >>> TODO: Asignar y remover empleados a puntos del grafo
# >>> TODO: Elegir personas a llevar(solo el conductor) y usar algoritmo de djistra para optimizar la ruta
