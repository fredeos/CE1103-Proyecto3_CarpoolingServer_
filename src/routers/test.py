import json

with open("src/database/bootup.txt", 'r') as file:
    for line in file:
        line = line.strip()
        strings = line.split(":")
        print(strings[0])
        # Load the json data
        path = f"src/database/{strings[0]}.json"
        with open(path, "r") as json_data:
            json_file = json.load(json_data)
        print("ID: ",json_file["id"])
        print(strings[1])
        if strings[1]=="driver":
            print("This person is a driver")
        