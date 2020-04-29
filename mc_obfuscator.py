import json
from os import urandom

from flask import Flask
from web.blueprints.faq import faq_blueprint
from web.blueprints.information import information_blueprint
from web.blueprints.tool import tool_blueprint

# Loading config:

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")
app.secret_key = urandom(40)
app.register_blueprint(tool_blueprint)
app.register_blueprint(information_blueprint)
app.register_blueprint(faq_blueprint)
# app.run()


if __name__ == '__main__':
    # serve(app)
    app.run()
    pass
