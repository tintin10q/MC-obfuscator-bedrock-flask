from minecraft_obfuscate.IDgenerator import get_new_random_name
from database.database_manager import config
import os
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
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        open(self.output_file_path, "w+").write(self.text)

    def obfuscate(self, context):
        for obfuscate_object in context["obfuscate_objects"]:
            self.text = obfuscate_object.obfuscate(self.text)
        self.sync_file_name(context["key"]["functions"])
        self.check_blacklist()
        return

    def check_blacklist(self):
        # This will change the output path
        function_blacklist = config["blacklist"]["functions"]
        if self.call_name in function_blacklist: # or True to disable for debugging
            self.output_file_path = self.set_file_path(self.call_name)
            self.output_path = os.path.split(self.output_file_path)[0]
            return
        if config["greedy_blacklist"]:
            for i in function_blacklist:
                if i in self.call_name:
                    print(i,self.call_name)
                    self.output_file_path = self.set_file_path(self.call_name)
                    self.output_path = os.path.split(self.output_file_path)[0]
                    print("Output path {}".format(self.output_file_path))
                    return

    def sync_file_name(self, function_call_names):
        # if no blacklist search found continue
        for function_call_name in function_call_names:
            if self.call_name == function_call_name[0]:
                self.name = function_call_name[1]
                self.output_file_path = self.set_file_path(self.name)
                return

    def set_file_path(self,file_name):
        return self.output_path + "\\" + file_name + ".mcfunction"
