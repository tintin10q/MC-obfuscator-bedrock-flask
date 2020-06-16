import io
import os
import re
from utils.IDgenerator import id_gen


class FunctionFile:
    objective_patterns = (
        r"scoreboard objectives (?:remove|add) (\S+)",
        r"scoreboard objectives setdisplay (?:sidebar|belowname|list) (\S+)",
        r"scoreboard players (?:reset|test|random|set|add|remove) \S+ (\S+)",
        r"scoreboard players operation \S+ (\S+)",
        r"scoreboard players operation \S+ \S+ (?:%=|\*=|\+=|-=|/=|<|=|>|><) \S+ (\S+)",
        r"scores=({.+})"
    )

    tag_patterns = (
        r"tag=!?(\w+)",
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

    patterns = {
        "objectives": [re.compile(pattern) for pattern in objective_patterns],
        "tags": [re.compile(pattern) for pattern in tag_patterns],
        "fake_players": [re.compile(pattern) for pattern in fake_player_patterns],
        "functions": [re.compile(pattern) for pattern in function_patterns]
    }

    group_6_p = re.compile(r'([{^=.,}]+)=')

    def __init__(self, path, text):
        self.names_in_file = set()
        self.call_name = path
        self.call_name = self.call_name.replace(".mcfunction", "")
        self.call_name = self.call_name.replace("\\", r"/")
        self.call_name = self.call_name  # Name used by other functions
        self.name = id_gen()  # Function name
        self.text = text  # Function text
        self.text = self.text.replace("\r\n", "\n")  # Fix for the \r\n to \n
        self.output_file_path = self.set_file_path(self.name)  # Path to the output file

    def __repr__(self):
        return self.text

    def obfuscate(self, context):
        for obfuscate_object in context["obfuscate_objects"]:
            if obfuscate_object.name in self.names_in_file:  # Only search if name is in set, all the work for this line
                self.text = obfuscate_object.obfuscate(self.text)  # But it is great now
        self.sync_file_name(context["key"]["functions"])
        self.check_blacklist(context["blacklist"]["functions"])
        return

    def find_obfuscate_objects(self, name_type, blacklist):
        assert name_type in FunctionFile.patterns, "{} not one of {}".format(name_type, FunctionFile.patterns.keys())
        patterns = FunctionFile.patterns[name_type]
        results = [re.findall(r, self.text) for r in patterns]

        if name_type == 'objectives' and len(results[5]): # Fix for group 6 find scores in selector problem
            results[5] = self.fix_group_6(results[5])
        results = {item for sublist in results for item in sublist}
        # Start looking at the blacklist
        if blacklist["whitelist"]:
            whitelist = {item for item in results if item in blacklist["blacklist"]}
            if blacklist["greedy"]:
                for item in results:
                    for whitelist_item in blacklist["blacklist"]:
                        if whitelist_item in item:
                            whitelist.add(item)
            results = whitelist
        else:
            for blacklist_item in blacklist["blacklist"]:
                if blacklist_item in results:
                    results.remove(blacklist_item)
                if blacklist["greedy"]:
                    results = {result for result in results if blacklist_item not in result}

        self.names_in_file = self.names_in_file | results  # Save results in class
        return results

    def check_blacklist(self, blacklist):
        # This will change the output path
        function_blacklist = blacklist["blacklist"]
        greedy = blacklist["greedy"]
        if self.call_name in function_blacklist:  # or True to disable for debugging
            self.output_file_path = self.set_file_path(self.call_name)
            return
        if greedy:
            for i in function_blacklist:
                if i in self.call_name:
                    self.output_file_path = self.set_file_path(self.call_name)
                    return

    def sync_file_name(self, function_call_names):
        # if no blacklist search found continue
        for function_call_name in function_call_names.items():
            if self.call_name == function_call_name[0]:
                self.name = function_call_name[1]
                self.output_file_path = self.set_file_path(self.name)
                return

    @staticmethod
    def fix_group_6(group_6):
        output = set()
        for scores in group_6:
            for j in re.findall(FunctionFile.group_6_p, scores):
                output.add(j)
        return output
            
            
    def set_file_path(self, file_name):
        return file_name + ".mcfunction"
