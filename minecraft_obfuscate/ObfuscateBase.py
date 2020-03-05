import re
from minecraft_obfuscate.IDgenerator import IDgenerator
from database.database_manager import config

class ObfuscateBase(IDgenerator):

    def __init__(self, name: str, regex_patterns):
        super().__init__()
        self.name = name
        self.len = len(self.name)
        self.regex_patterns = regex_patterns
        self.new_name = self.get_new_random_name()
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
        if config["remove_comments"]:
            text = re.sub(re.compile("#.{0,}\n?"), "", text)
        # Remove blank lines
        blanklines_pat = re.compile("\n\n")
        while re.search(blanklines_pat,text) is not None:
            text = re.sub(blanklines_pat,"\n",text)
        if text[0] =="\n":
            text = text[1:]
        return text
