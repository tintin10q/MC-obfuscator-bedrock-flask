from minecraft_obfuscate.IDgenerator import get_new_random_name
from database.database_manager import config

class FunctionFile:

    def __init__(self, path, output_path):
        self.call_name = path.replace(config["target_path"], "")
        self.call_name = self.call_name.replace(".mcfunction", "")
        self.call_name = self.call_name.replace("\\",r"/")
        self.call_name = self.call_name[1:]  # Name used by other functions
        self.name = get_new_random_name()  # Function name
        self.text = open(path, "r+").read()  # Function text
        self.output_path = output_path  # Path to the output folder
        self.output_file_path = self.set_file_path(self.name)  # Path to the output file

    def __repr__(self):
        return self.text

    def write_file(self):
        open(self.output_file_path, "w+").write(self.text)

    def obfuscate(self, context):
        for obfuscate_object in context["obfuscate_objects"]:
            self.text = obfuscate_object.obfuscate(self.text)
        return

    def sync_file_name(self, function_call_names):
        for i in function_call_names:
            if self.call_name == i[0]:
                self.name = i[1]
                self.output_path = self.set_file_path(self.name)

    def set_file_path(self,file_name):
        return self.output_path + "\\" + file_name + ".mcfunction"
