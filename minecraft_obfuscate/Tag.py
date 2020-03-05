from minecraft_obfuscate.Objective import ObfuscateBase


class Tag(ObfuscateBase):
    def __init__(self, name):
        regex_patters = (
            r"(.\[\S*tag=!?)({name})(\S*\])",
            r"(tag \S+ (?:add|remove) )({name})()",

            r"(.\[\S*name=!?)({name})(\S*\])",
            r"(summon\s\S+\s[\~\^]?[\+\-]{{0,}}[0-9]{{0,}}\s[\~\^]?[\+\-]{{0,}}[0-9]{{0,}}\s[\~\^]?[\+\-]{{0,}}[0-9]{{0,}}\s\S+\s)({name})()"

        )
        super().__init__(name, regex_patters)
