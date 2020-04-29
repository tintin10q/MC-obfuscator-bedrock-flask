import re

from utils.IDgenerator import id_gen


class ObfuscateBase():
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
        while "\n\n" in text:
            text = text.replace("\n\n","\n")
        return text
