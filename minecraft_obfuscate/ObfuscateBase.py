import re
from minecraft_obfuscate.IDgenerator import IDgenerator


class ObfuscateBase(IDgenerator):

    def __init__(self, name: str, regex_patterns):
        super().__init__()
        self.name = name
        self.regex_patterns = regex_patterns
        self.new_name = self.get_new_random_name()
        self.key = (self.name, self.new_name)  # Used for the output key
        self.regex = [re.compile(r.format(name=self.name)) for r in regex_patterns]

    def __repr__(self):
        return self.name

    def obfuscate(self, text):
        for r in self.regex:
            text = r.sub(r"\g<1>{}\g<3>".format(self.new_name), text)
        return text
