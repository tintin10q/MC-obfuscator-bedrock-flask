from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import zipfile
import io
# from minecraft_obfuscate.obfuscate_zip import obfuscate_zip

# obfuscate_zip()

tool_blueprint = Blueprint('main', __name__)


@tool_blueprint.route("/", methods=["GET"])
def tool_post():
    print("cool")
    return render_template("tool.html")


def allowed_file(filename):
    if filename.split(".")[-1] in ("zip"):
        return True
    else:
        return False

@tool_blueprint.route("/", methods=["POST"])
def tool_get():
    # check if the post request has the file part
    if 'datapack_zip_file' not in request.files:
        flash('Could not find file with html name "datapack_zip_file"','danger') # Catogories danger, succes, warning and info
        return redirect(request.url)
    file = request.files['datapack_zip_file']
    # if user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        flash('No file was selected', "warning")
        return redirect(request.url)
    filename = secure_filename(file.filename)
    if not allowed_file(filename):
        flash('File does not end with a .zip file extension', "warning")
        return redirect(request.url)

    config = {'function_blacklist': '', 'greedy_functions': '', 'skip_functions': False, 'objective_blacklist': '',
              'greedy_objectives': False, 'skip_objectives': False, 'fakeplayers_blacklist': '',
              'greedy_fakeplayers': False, 'skip_fake_players': False, 'tag_blacklist': "", 'greedy_tags': False,
              'skip_tags': False, 'character_pool': 'O0', 'name_lenght': '16', 'datapack_zip_file': ''}

    # merge configs
    config.update(request.form.to_dict())
    # print(config)
    # format config a bit better
    config["blacklist"] = {"functions":config.pop("function_blacklist").split("\r\n"),
                           "objectives": config.pop("objective_blacklist").split("\r\n"),
                           "tags": config.pop("tag_blacklist").split("\r\n"),
                           "fakeplayers_blacklist": config.pop("fakeplayers_blacklist").split("\r\n"),
                           }  # please dont change \r\n that would be an annoying bug to fix
    file_like_object = file.stream._file
    zipfile_ob = zipfile.ZipFile(file_like_object)
    file_names = zipfile_ob.namelist()
    # Filter names to only include the filetype that you want:
    file_names = [file_name for file_name in file_names if file_name.endswith(".mcfunction")]

    files = [(zipfile_ob.open(name).read(),name) for name in file_names]
    return redirect(request.url)