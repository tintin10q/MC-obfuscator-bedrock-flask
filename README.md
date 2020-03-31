# bedrock-function-obfuscator
The obfuscation works with the minecraft_obfuscate module created by me

First turn every function file into a class.

You then then do all the required searches to find all the names in the text.
Then you create objects of those names.
Sort that list so name length problem is solved.
Then search for those names in all the files with those objects and replace them by the same name.
Write the functions and the consider the blacklist.

The process can start by providing a zip file and a config to:
obfuscate_start obfuscate_zip
it will return a zip with the obfuscation