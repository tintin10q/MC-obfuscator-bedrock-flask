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

    # Find all the names
    tags, objectives, fake_players, functions = set(), set(), set(), set()
    for function_file in function_files:  # | is used to merge sets
        tags = tags | function_file.find_obfuscate_objects("tags", blacklist["tags"])
        objectives = objectives | function_file.find_obfuscate_objects("objectives", blacklist["objectives"])
        fake_players = fake_players | function_file.find_obfuscate_objects("fake_players", blacklist["fake_players"])
        functions = functions | function_file.find_obfuscate_objects("functions", blacklist["functions"])

    obfuscate_objects = []
    obfuscate_objects += [Tag(tag) for tag in tags]
    obfuscate_objects += [FakePlayer(fake_player) for fake_player in fake_players]
    obfuscate_objects += [Function(function) for function in functions]
    obfuscate_objects += [Objective(objective) for objective in objectives]

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
