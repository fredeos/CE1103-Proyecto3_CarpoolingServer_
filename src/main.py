from fastapi import FastAPI
from fastapi import Query
import json

http_app = FastAPI()

employees = [] # This list saves dictionaries(jsons) of the employees of the app

drivers = [] # This list saves dictionaries(jsons) of the drivers of the app

id_counter = 0 # Variable for counting id

#-----------------[Reads from the saved files and adds them to the previous lists]-----------------#
with open("src/database/bootup.txt", "r") as file: #Read from the bootup file
    for line in file:
        line = line.strip() # This only removes whitespaces
        strings = line.split(":")

        path = f"src/database/{strings[0]}.json"
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
    user = {}
    for driver in drivers:
        if driver["id"]==id:
            user = driver
    return user

# >>> GET a employee by id
@http_app.get("/employees/")
def get_employee_by_id(id:int=Query()):
    user = {}
    for employee in employees:
        if employee["id"]==id:
            user = employee
    return user

# >>> Create new user account
@http_app.post("/accounts/new/")
def create_new_user(name:str=Query(...), type: str=Query(...), mail:str=Query(...)):
    # Save the profile information to a dictionary
    user = {
        "id": id_counter+1,
        "name": name,
        "mail": mail
    }
    # Output folder for saving the user json file
    output_path = f"src/database/{mail}.json"
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

#TODO: POST method for registering new accounts, GET method for login into an existing account