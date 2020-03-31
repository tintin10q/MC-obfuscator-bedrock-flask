import random


class IDgenerator:
    """An id generator that will never run out of ids to give and never give the same id not an actual generator :("""

    def __init__(self, character_pool="O0", length=16):
        self.character_pool = character_pool
        self.length = length
        self.used_UUIDs = []
        self.max_ids = 2 ** length

    def __call__(self):
        return self.get_new_random_name()

    def generate_random_name(self):
        uuid = ""
        for i in range(self.length):
            uuid += random.choice(self.character_pool)
        return uuid

    def get_new_random_name(self):
        uuid = None
        while uuid in self.used_UUIDs or uuid is None:
            uuid = self.generate_random_name()
        self.used_UUIDs.append(uuid)
        if len(self.used_UUIDs) == self.max_ids:  # Make the ids longer this way the generator will never run out
            self.used_UUIDs.clear()
            self.length += 1
            self.max_ids = 2 ** self.length
        return uuid

    def reset(self, character_pool="O0", length=16):
        self.__init__(character_pool, length)


id_gen = IDgenerator()
