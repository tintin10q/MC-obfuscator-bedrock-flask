import os
import io
from utils.IDgenerator import id_gen


class FunctionFile:

    def __init__(self, path, text):
        self.call_name = path
        self.call_name = self.call_name.replace(".mcfunction", "")
        self.call_name = self.call_name.replace("\\", r"/")
        self.call_name = self.call_name  # Name used by other functions
        self.name = id_gen() # Function name
        self.text = text  # Function text
        self.text = self.text.replace("\r\n", "\n")  # Fix for the \r\n to \n
        self.output_file_path = self.set_file_path(self.name)  # Path to the output file

    def __repr__(self):
        return self.text

    def obfuscate(self, context):
        for obfuscate_object in context["obfuscate_objects"]:
            self.text = obfuscate_object.obfuscate(self.text)
        self.sync_file_name(context["key"]["functions"])
        self.check_blacklist(context["blacklist"]["functions"])
        return

    def check_blacklist(self, blacklist):
        # This will change the output path
        function_blacklist = blacklist["blacklist"]
        greedy = blacklist["greedy"]
        if self.call_name in function_blacklist:  # or True to disable for debugging
            self.output_file_path = self.set_file_path(self.call_name)
            return
        if greedy:
            for i in function_blacklist:
                if i in self.call_name:
                    self.output_file_path = self.set_file_path(self.call_name)
                    return

    def sync_file_name(self, function_call_names):
        # if no blacklist search found continue
        for function_call_name in function_call_names.items():
            if self.call_name == function_call_name[0]:
                self.name = function_call_name[1]
                self.output_file_path = self.set_file_path(self.name)
                return

    def set_file_path(self, file_name):
        return file_name + ".mcfunction"
