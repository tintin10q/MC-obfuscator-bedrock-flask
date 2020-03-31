import glob
import io
import json
import operator
import os
import re
import zipfile

from minecraft_obfuscate.FakePlayer import FakePlayer
from minecraft_obfuscate.Function import Function
from minecraft_obfuscate.FunctionFile import FunctionFile
from minecraft_obfuscate.Objective import Objective
from minecraft_obfuscate.Tag import Tag


def find_obfuscate_objects(text, patterns, blacklist):
    patterns = [re.compile(r) for r in patterns]
    results = [re.findall(r, text) for r in patterns]
    results = [item for sublist in results for item in sublist]  # Flatten the list
    results = list(set(results))  # Remove duplicates
    if blacklist["skip"]:
        return results
    else:
        for blacklist_item in blacklist["blacklist"]:
            if blacklist_item in results:
                results.remove(blacklist_item)
            if blacklist["greedy"]:
                results = [result for result in results if blacklist_item not in result]
    return results


def sterilize(obj):
    object_type = type(obj)
    if isinstance(obj, dict):
        return {k: sterilize(v) for k, v in obj.items()}
    elif object_type in (list, tuple):
        return [sterilize(v) for v in obj]
    elif object_type in (str, int, bool):
        return obj
    else:
        return obj.__repr__()


def obfuscate_zip(zip_files, config):
    blacklist = config["blacklist"]
    function_files = [FunctionFile(path=zip_file[0], text=zip_file[1]) for zip_file in zip_files]

    all_text = ""
    for function_file in function_files:
        all_text += function_file.text + "\n"  # Damm that was a nasty one for sure with the \n
    # All the patterns
    objective_patterns = (
        r"scoreboard objectives (?:remove|add) (\S+)",
        r"scoreboard objectives setdisplay (?:sidebar|belowname|list) (\S+)",
        r"scoreboard players (?:reset|test|random|set|add) \S+ (\S+)",
        r"scoreboard players operation \S+ (\S+)",
        r"scoreboard players operation \S+ \S+ (?:%=|\*=|\+=|-=|/=|<|=|>|><) \S+ (\S+)",
    )

    tag_patterns = (
        r"tag=(\w+)",
        r"tag \S+ (?:add|remove) (\S+)",
        r"name=(\w+)",
        r"summon\s\S+\s[\~\^]?[\+\-]{0,}[0-9]{0,}\s[\~\^]?[\+\-]{0,}[0-9]{0,}\s[\~\^]?[\+\-]{0,}[0-9]{0,}\s\S+\s(\w+)"
    )

    fake_player_patterns = (
        r"scoreboard players (?:reset|test|random|set|add) ([^@]\S+)",
        r"scoreboard players operation ([^@]\S+)",
        r"scoreboard players operation \S+ \S+ (?:%=|\*=|\+=|-=|/=|<|=|>|><) ([^@]\S+)"
    )

    # if you only have one pattern make sure to make it a list! #
    function_patterns = [
        r"function (\S+)"
    ]

    # Find all the names
    tags = find_obfuscate_objects(all_text, tag_patterns, blacklist["tags"])
    objectives = find_obfuscate_objects(all_text, objective_patterns, blacklist["objectives"])
    fake_players = find_obfuscate_objects(all_text, fake_player_patterns, blacklist["fake_players"])
    functions = find_obfuscate_objects(all_text, function_patterns, blacklist["functions"])
    obfuscate_objects = []
    for tag in tags:
        obfuscate_objects.append(Tag(tag))
    for objective in objectives:
        obfuscate_objects.append(Objective(objective))
    for fake_player in fake_players:
        obfuscate_objects.append(FakePlayer(fake_player))
    for function in functions:
        obfuscate_objects.append(Function(function))

    obfuscate_objects.sort(key=operator.attrgetter('len'),
                           reverse=True)  # sort the list so longer names get replaced first

    # Generate key
    context = {
        "key": {"objectives": {objective.key[0]: objective.key[1] for objective in obfuscate_objects if
                               isinstance(objective, Objective)},
                "tags": {tag.key[0]: tag.key[1] for tag in obfuscate_objects if isinstance(tag, Tag)},
                "fake_players": {fake_player.key[0]: fake_player.key[1] for fake_player in obfuscate_objects if
                                 isinstance(fake_player, FakePlayer)},
                "functions": {function.key[0]: function.key[1] for function in obfuscate_objects if
                              isinstance(function, Function)}},
        "obfuscate_objects": obfuscate_objects,
        "blacklist": blacklist}
    zip_buffer = io.BytesIO()
    print(context)
    with zipfile.ZipFile(zip_buffer, mode='w') as zf:
        for function_file in function_files:
            function_file.obfuscate(context)
            zf.writestr(function_file.output_file_path, function_file.text)
        if "context-file" in config:
            output_context = {k: sterilize(v) for k, v in context.items()}
            output_context.pop("obfuscate_objects")
            zf.writestr(".name_changes.json", json.dumps(output_context, indent=4))
    zip_buffer.seek(0)
    return zip_buffer
