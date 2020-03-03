import glob
import os
import re

from database.database_manager import db
from minecraft_obfuscate.FakePlayer import FakePlayer
from minecraft_obfuscate.Function import Function
from minecraft_obfuscate.FunctionFile import FunctionFile
from minecraft_obfuscate.Objective import Objective
from minecraft_obfuscate.Tag import Tag

db.reset()

config = db.get("config")
target_path = config["target_path"]
output_path = config["output_path"]
blacklist = config["blacklist"]

if target_path is None or output_path is None:
    raise Exception("The config.json is not propper 'target_path' and 'output_path' must have paths")

globs = glob.glob(target_path + "\\**\\*.mcfunction", recursive=True)
obfuscate_objects = []

if not os.path.exists(output_path):
    os.makedirs(output_path)

function_files = [FunctionFile(glob, output_path) for glob in globs]

all_text = ""
for function_file in function_files:
    all_text += function_file.text


def find_obfuscate_objects(patterns, blacklist_type=""):
    patterns = [re.compile(r) for r in patterns]
    results = [re.findall(r, all_text) for r in patterns]
    results = [item for sublist in results for item in sublist]  # Flatten the list
    results = list(set(results))  # Remove duplicates
    if blacklist_type in ("objectives", "tags", "fake_players", "functions"):
        for blacklist_item in blacklist[blacklist_type]:
            if blacklist_item in results:
                results.remove(blacklist_item)
            if config["greedy_blacklist"]:
                results = [result for result in results if blacklist_item not in result]
    return results


objective_patterns = (
    r"scoreboard objectives (?:remove|add) (\S+)",
    r"scoreboard objectives setdisplay (?:sidebar|belowname|list) (\S+)",
    r"scoreboard players (?:reset|test|random|set|add) \S+ (\S+)",
    r"scoreboard players operation \S+ (\S+)",
    r"scoreboard players operation \S+ \S+ (?:%=|\*=|\+=|-=|/=|<|=|>|><) \S+ (\S+)",
)

tag_patterns = (
    r"tag=(\w+)",
    r"tag \S+ (?:add|remove) (\S+)"
)

fake_player_patterns = (
    r"scoreboard players (?:reset|test|random|set|add) ([^@]\S+)",
    r"scoreboard players operation ([^@]\S+)",
    r"scoreboard players operation \S+ \S+ (?:%=|\*=|\+=|-=|/=|<|=|>|><) ([^@]\S+)"
)

function_patterns = [
    r"function (.+)"
]

tags = find_obfuscate_objects(tag_patterns, "tags")
objectives = find_obfuscate_objects(objective_patterns, "objectives")
fake_players = find_obfuscate_objects(fake_player_patterns, "fake_players")
functions = find_obfuscate_objects(function_patterns, "functions")

for tag in tags:
    obfuscate_objects.append(Tag(tag))
for objective in objectives:
    obfuscate_objects.append(Objective(objective))
for fake_player in fake_players:
    obfuscate_objects.append(FakePlayer(fake_player))
for function in functions:
    obfuscate_objects.append(Function(function))

# Generate key
context = {"key": {"objectives": [objective.key for objective in obfuscate_objects if isinstance(objective, Objective)],
                   "tags": [tag.key for tag in obfuscate_objects if isinstance(tag, Tag)],
                   "fake_players": [fake_player.key for fake_player in obfuscate_objects if
                                    isinstance(fake_player, FakePlayer)],
                   "functions": [function.key for function in obfuscate_objects if isinstance(function, Function)]},
           "obfuscate_objects": obfuscate_objects,
           "blacklist": blacklist}

import pprint
# pprint.pprint(context)

for function_file in function_files:
    function_file.obfuscate(context)
    function_file.write_file()

"""
To do:

- Test if functions actually work in Minecraft
- Output the context.json with date
- Build a gui 
- make blacklist work with function names
- Build a web gui (without tkinter go fuck yourself) web gui?? this would solve problems

-1 1
-3 2

"""


