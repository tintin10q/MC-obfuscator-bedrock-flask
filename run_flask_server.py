from flask import Flask
import json
from os import urandom
from web.blueprints.tool import tool_blueprint

# Loading config:

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")
app.secret_key = urandom(40)
app.register_blueprint(tool_blueprint)
# app.run()


if __name__ == '__main__':
    # serve(app)
    app.run()
    pass