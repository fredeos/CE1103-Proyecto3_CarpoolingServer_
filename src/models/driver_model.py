import json
from pydantic import BaseModel

class Driver(BaseModel):
    id: int
    name: str
    mail: str

    def build_from_json(self, json_string:str):
        pass