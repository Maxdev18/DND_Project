import json
import random

def get_role(class_type = ""):
  with open('./util/roles.json') as f:
    d = json.load(f)
    response = ""

    for role in d["roles"]:
       type = role["class_type"]
       response += f"* {type}\n"

    if class_type != "":
       print("Inside the role here")
       return class_type
       
    return response

def get_sidekicks(sidekick_name = ""):
   with open('./util/sidekick.json') as f:
    d = json.load(f)

    response = ""

    for sidekick in d["sidekick"]:
       name = sidekick["sidekick_name"]
       response += f"* {name}\n"

    print("Response:", response)

    if sidekick_name != "":
       print("Inside the sidekick_name here")
       return sidekick_name

    return response

def get_potions(potion_name = ""):
   with open('./util/potions.json') as f:
    d = json.load(f)
    response = ""

    # TODO: Need to randomly select either here or have the DM select the potions.

    for sidekick in d["potions"]:
       name = sidekick["potion_name"]
       response += f"* {name}\n"

    print("Response:", response)

    if potion_name != "":
       print("Inside the potion_name here")
       return potion_name

    return response

def roll_for(skill, dc, player):
    n_dice = 1
    sides = 20
    roll = sum([random.randint(1, sides) for _ in range(n_dice)])
    if roll >= int(dc):
        return f'{player} rolled {roll} for {skill} and succeeded!'
    else:
        return f'{player} rolled {roll} for {skill} and failed!'