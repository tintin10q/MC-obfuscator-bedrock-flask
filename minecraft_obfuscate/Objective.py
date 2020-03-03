from minecraft_obfuscate.ObfuscateBase import ObfuscateBase


class Objective(ObfuscateBase):
    def __init__(self, name):
        regex_patterns = (
            r"(scoreboard objectives (?:remove|add) )({name})()",
            r"(scoreboard objectives setdisplay (?:sidebar|belowname|list) )({name})()",
            r"(scoreboard players (?:reset|test|random|set|add) \S+ )({name})()",
            r"(scoreboard players operation \S+ )({name})()",
            r"(scoreboard players operation \S+ \S+ (?:%=|\*=|\+=|-=|/=|<|=|>|><) \S+ )({name})()",
            r"(\[\S*scores=[{{]\S*\b)({name})(\b\S+}})"
        )
        super().__init__(name, regex_patterns)
