import json
import random
 
class Character:
  def __init__(self):
    try:
      with open("util/roles.json", "r") as file:
        data = json.load(file)
        num = random.randint(0, 3) # get a random role from the roles list in the json file
        self.class_type = data["roles"][num]["class_type"] 
        self.health = data["roles"][num]["health"]
        self.damage = data["roles"][num]["damage"]

    except Exception as e:
      print(e)

 