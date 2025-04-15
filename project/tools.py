import json
import random
from huggingface_hub import InferenceClient

HUGGING_FACE_API_TOKEN = "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"

def generate_image(prompt, filename="generated_image.png"):
   client = InferenceClient(
      provider="hf-inference",
      api_key=HUGGING_FACE_API_TOKEN,
   )

   image = client.text_to_image(
      prompt,
      model="black-forest-labs/FLUX.1-dev",
   )

   # Convert the bytes to an image and save
   image.save(filename)
   print(f"✅ Image saved to {filename}")
   return filename

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

def get_sidekicks(sidekick_name=""):
    with open('./util/sidekick.json') as f:
      d = json.load(f)

    response = ""
    all_names = []

    for sidekick in d["sidekick"]:
      name = sidekick["sidekick_name"]
      all_names.append(name)
      response += f"* {name}\n"

      print("Generating image for:", name)
      generate_image(f"Create a portrait of a character named {name}, stylized for a fantasy DND game.", filename=f"{name}_image.png")

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