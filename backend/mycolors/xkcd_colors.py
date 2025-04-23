# xkcd_colors = {
#     "Blush Pink": "#f6a6b6",
#     "Ocean Blue": "#03719c",
#     "Forest Green": "#06470c",
#     "Pale Red": "#d9544d",
#     "Dusty Orange": "#f0833a",
#     "Lemon Yellow": "#fff44f",
#     "Slate Blue": "#5b7c99",
#     "Light Lavender": "#dfc5fe",
#     "Mint Green": "#8fff9f",
#     "Deep Rose": "#c74767",
#     "Sky Blue": "#75bbfd",
#     "Warm Grey": "#9e8e86",
#     "Sunflower": "#ffda03",
#     "Pumpkin Orange": "#fb7d07",
#     "Cool Cyan": "#4eccc6",
#     "Charcoal": "#343837",
#     "Bubblegum Pink": "#fe83cc",
#     "Cobalt Blue": "#1e488f",
#     "Emerald": "#01a049",
#     "Moss Green": "#658b38",
#     "Burnt Sienna": "#b04e0f",
#     "Periwinkle": "#8e82fe",
#     "Coral Pink": "#ff6163",
#     "Peach": "#ffb07c",
#     "Denim Blue": "#3b5b92",
#     "Turquoise": "#06c2ac",
#     "Goldenrod": "#fac205",
#     "Rust Red": "#a13905",
#     "Lavender Grey": "#c4c3d0",
#     "Teal Green": "#25a36f",
#     "Rose": "#cf6275",
#     "Plum": "#580f41",
# }


import json
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the JSON file in the same folder
file_path = os.path.join(script_dir, "color_names.json")

print(f"file_path: {file_path}")
# Load the JSON content
with open(file_path, "r") as f:
    colors = json.load(f)


xkcd_colors = {item["color"]: item["hex"] for item in colors}
# print(xkcd_colors)
