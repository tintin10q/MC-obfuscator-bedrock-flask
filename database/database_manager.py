import json
import os


class Database():
    # This class is used to write and read stuff with the database
    my_path = os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def get(name):
        """Will return a database with the name given. So get(users) with get users.json"""
        database_path = os.path.join(os.path.dirname(__file__), name + ".json")
        database_file = open(database_path, "r+")
        database = json.load(database_file)
        return database

    @staticmethod
    def set(name, data):
        """Will set a database with the name given. So set(users,database) with set users.json with database"""
        database_path = os.path.join(os.path.dirname(__file__), name + ".json")
        json.dump(data, open(database_path, "w+"), indent=4, sort_keys=True)

    @staticmethod
    def insert(name, data):
        """ Will append database to a list named <name> in a file named <name>.json """
        database = Database.get(name)
        database[name].append(data)
        Database.set(name, database)
        # self.set(name,self.get(name)[name].append(database))

    @staticmethod
    def remove(naam):
        """A function that will try and remove a name from the players.json"""
        # persons only
        data = Database.get("players")
        try:
            data["people"].pop(naam)
            Database.set(data, "players")
            return True
        except:
            return False

    @staticmethod
    def reset():
        """Will reset all databases. They should be registered manually"""
        Database.set("used_uuids", {"used_uuids": []})
        return

    @staticmethod
    def translate(name):
        """ Will translate a name to the corresponding ID """
        translations = Database.get("translations")
        if name in translations:
            return translations[name]
        else:
            return False


db = Database()

# Will capture config as it is on startup for live config do db.get("config")
if not os.path.exists(Database.my_path + "\\config.json"):
    print("created new config")
    new_config = {
    "blacklist": {
        "fake_players": [],
        "functions": [],
        "objectives": [],
        "tags": []
    },
    "output_context": False,
    "remove_comments": True,
    "character_length": 16,
    "character_pool": "0O",
    "greedy_blacklist": False,
    "output_path": "",
    "target_path": ""}
    db.set("config", new_config)
config = db.get("config") if os.path.exists(str(Database.my_path) + "/config.json") else {}
