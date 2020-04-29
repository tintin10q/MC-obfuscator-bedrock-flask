import io
import zipfile

from flask import Blueprint, render_template, request, redirect, flash, send_file, Response
from minecraft_obfuscate.obfuscate_zip import obfuscate_zip
from utils.IDgenerator import id_gen
from utils.allowed_file import allowed_file
from werkzeug.utils import secure_filename

# obfuscate_zip()

tool_blueprint = Blueprint('main', __name__)


@tool_blueprint.route("/", methods=["GET"])
def tool_get():
    return render_template("tool.html")


@tool_blueprint.route("/", methods=["POST"])
def tool_post():
    # check if the post request has the file part
    if 'datapack_zip_file' not in request.files:
        flash('Could not find file with html name "datapack_zip_file"', 'danger')
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

    config = {'function_blacklist': '', 'greedy_functions': False, 'whitelist_functions': False,
              'objective_blacklist': '',
              'greedy_objectives': False, 'whitelist_objectives': False, 'fake_players_blacklist': '',
              'greedy_fake_players': False, 'whitelist_fake_players': False, 'tag_blacklist': "", 'greedy_tags': False,
              'whitelist_tags': False, 'character_pool': 'O0', 'name_length': 16, 'datapack_zip_file': ''}

    config.update(request.form.to_dict())
    #  Confirm that name length is an int
    if type(config["name_length"]) == str:
        try:
            config["name_length"] = int(config["name_length"])
        except:
            flash("Name length was not a number!", "warning")
            return redirect(request.url)

    # format config a bit better # please dont change \r\n that would be an annoying bug to fix
    config["blacklist"] = {"functions": {"blacklist": config.pop("function_blacklist").split("\r\n"),
                                         "greedy": config.pop("greedy_functions"),
                                         "whitelist": config.pop("whitelist_functions"),
                                         },
                           "objectives": {"blacklist": config.pop("objective_blacklist").split("\r\n"),
                                          "greedy": config.pop("greedy_objectives"),
                                          "whitelist": config.pop("whitelist_objectives"),
                                          },
                           "tags": {"blacklist": config.pop("tag_blacklist").split("\r\n"),
                                    "greedy": config.pop("greedy_tags"),
                                    "whitelist": config.pop("whitelist_tags"),
                                    },
                           "fake_players": {"blacklist": config.pop("fake_players_blacklist").split("\r\n"),
                                            "greedy": config.pop("greedy_fake_players"),
                                            "whitelist": config.pop("whitelist_fake_players")}}
    #  Magic zip code
    file_like_object = file.stream._file
    zipfile_ob = zipfile.ZipFile(file_like_object)
    file_names = zipfile_ob.namelist()
    # Filter names to only include the filetype that you want:
    file_names = [file_name for file_name in file_names if file_name.endswith(".mcfunction")]
    files = [(path, zipfile_ob.open(path).read().decode("utf-8")) for path in file_names]
    #  Reset id_gen
    id_gen.reset(config["character_pool"], config["name_length"])

    final_zip = obfuscate_zip(files, config)
    return send_file(final_zip, mimetype='application/zip', attachment_filename=filename, as_attachment=True)
