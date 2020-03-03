from minecraft_obfuscate.ObfuscateBase import ObfuscateBase


class FakePlayer(ObfuscateBase):
    def __init__(self, name):
        regex_patterns = (
            r"(scoreboard players (?:reset|test|random|set|add) [^@]?)({name})()",
            r"(scoreboard players operation [^@]?)({name})()",
            r"(scoreboard players operation \S+ \S+ (?:%=|\*=|\+=|-=|/=|<|=|>|><) [^@]?)({name})()"
        )
        super().__init__(name, regex_patterns)
