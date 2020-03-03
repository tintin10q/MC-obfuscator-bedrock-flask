import random
from database.database_manager import db
from database.database_manager import config

character_length = config["character_length"]

class IDgenerator:

    obfuscate_characters = config["character_pool"]  # other options include O0, vw, mn,

    def __call__(self, length=character_length):
        return self.get_new_random_name(length)

    @staticmethod
    def generate_random_name(lenght=character_length):
        uuid = ""
        for i in range(0, lenght):
            uuid += random.choice(IDgenerator.obfuscate_characters)
        return uuid

    @staticmethod
    def get_new_random_name(lenght=character_length):
        uuid = ""
        used_uuids = db.get("used_uuids")
        while uuid in used_uuids or uuid == "":
            uuid = IDgenerator.generate_random_name(lenght)
        db.insert("used_uuids", uuid)
        return uuid


def generate_random_name(lenght=character_length):
    uuid = ""
    for i in range(0, lenght):
        uuid += random.choice(IDgenerator.obfuscate_characters)
    return uuid


def get_new_random_name(lenght=character_length):
    uuid = ""
    used_uuids = db.get("used_uuids")
    while uuid in used_uuids or uuid == "":
        uuid = generate_random_name(lenght)
    db.insert("used_uuids", uuid)
    return uuid