import io
import zipfile

from flask import Blueprint, render_template, request, redirect, flash
from minecraft_obfuscate.obfuscate_zip import obfuscate_zip
from werkzeug.utils import secure_filename
from minecraft_obfuscate.IDgenerator import id_gen
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
        flash('Could not find file with html name "datapack_zip_file"',
              'danger')  # Catogories danger, succes, warning and info
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

    config = {'function_blacklist': '', 'greedy_functions': False, 'skip_functions': False, 'objective_blacklist': '',
              'greedy_objectives': False, 'skip_objectives': False, 'fake_players_blacklist': '',
              'greedy_fake_players': False, 'skip_fake_players': False, 'tag_blacklist': "", 'greedy_tags': False,
              'skip_tags': False, 'character_pool': 'O0', 'name_lenght': 16, 'datapack_zip_file': ''}

    config.update(request.form.to_dict())

    #  Confirm that name lenght is an int
    if type(config["name_lenght"]) == str:
        try:
            config["name_lenght"] = int(config["name_lenght"])
        except:
            flash("Name lenght was not a number!", "warning")
            return redirect(request.url)

    # format config a bit better # please dont change \r\n that would be an annoying bug to fix
    config["blacklist"] = {"functions": {"blacklist": config.pop("function_blacklist").split("\r\n"),
                                         "greedy": config.pop("greedy_functions"),
                                         "skip": config.pop("skip_functions"),
                                         },
                           "objectives": {"blacklist": config.pop("objective_blacklist").split("\r\n"),
                                          "greedy": config.pop("greedy_objectives"),
                                          "skip": config.pop("skip_objectives"),
                                          },
                           "tags": {"blacklist": config.pop("tag_blacklist").split("\r\n"),
                                    "greedy": config.pop("greedy_tags"),
                                    "skip": config.pop("skip_tags"),
                                    },
                           "fake_players": {"blacklist": config.pop("fake_players_blacklist").split("\r\n"),
                                           "greedy": config.pop("greedy_fake_players"),
                                           "skip": config.pop("skip_fake_players")}}
    #  Magic zip code
    file_like_object = file.stream._file
    zipfile_ob = zipfile.ZipFile(file_like_object)
    file_names = zipfile_ob.namelist()
    # Filter names to only include the filetype that you want:
    file_names = [file_name for file_name in file_names if file_name.endswith(".mcfunction")]
    files = [(path, zipfile_ob.open(path).read().decode("utf-8")) for path in file_names]

    #  Reset id_gen
    id_gen.reset(config["character_pool"], config["name_lenght"])

    print(id_gen.used_UUIDs)
    obfuscate_zip(files, config)
    return redirect(request.url)
