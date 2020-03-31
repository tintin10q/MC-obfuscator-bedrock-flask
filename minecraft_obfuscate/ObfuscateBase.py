import re

from utils.IDgenerator import id_gen


class ObfuscateBase():
    blanklines_pattern = re.compile("\n\n")
    comment_pattern = re.compile("#.{0,}\n?")

    def __init__(self, name: str, regex_patterns):
        self.name = name
        self.len = len(self.name)
        self.regex_patterns = regex_patterns
        self.new_name = id_gen()
        self.key = (self.name, self.new_name)  # Used for the output key
        self.regex = [re.compile(r.format(name=self.name)) for r in regex_patterns]

    def __repr__(self):
        return self.name

    def __len__(self):
        return self.len

    def obfuscate(self, text):
        for r in self.regex:
            text = r.sub(r"\g<1>{}\g<3>".format(self.new_name), text)
        # Remove comments
        if True:  # TODO: config["remove_comments"]
            text = re.sub(ObfuscateBase.comment_pattern, "", text)
        # Remove blank lines

        while re.search(ObfuscateBase.blanklines_pattern, text) is not None:
            text = re.sub(ObfuscateBase.blanklines_pattern, "\n", text)
        if text[0] == "\n":
            text = text[1:]
        return text
