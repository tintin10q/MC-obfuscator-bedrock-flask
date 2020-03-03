from minecraft_obfuscate.ObfuscateBase import ObfuscateBase


class Function(ObfuscateBase):
    def __init__(self, name):
        regex_patterns = [
            r"(function )({name})()"
        ]
        super().__init__(name, regex_patterns)
