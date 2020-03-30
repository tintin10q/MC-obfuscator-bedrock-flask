from flask import Flask, request
app = Flask(__name__)

@app.route("/",methods=["GET"])
def page_name_get():
    return """<form action="." method="post" enctype=multipart/form-data>
        <input type="file" accept="application/zip" name="data_zip_file" accept="application/zip" required>
         <button type="submit">Send zip file!</button>
        </form>"""

import zipfile

@app.route("/",methods=["POST"])
def page_name_post():
    file = request.files['data_zip_file']

    file_like_object = file.stream._file
    zipfile_ob = zipfile.ZipFile(file_like_object)
    file_names = zipfile_ob.namelist()
    # Filter names to only include the filetype that you want:
    file_names = [file_name for file_name in file_names if file_name.endswith(".mcfunction")]

    files = [(zipfile_ob.open(name).read(),name) for name in file_names]
    return str(files)





# app.run()