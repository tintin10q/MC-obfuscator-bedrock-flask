from waitress import serve
from database.database_manager import db
from flask import Flask

from web.blueprints.tool import tool_blueprint

# Loading config:
web_config = db.get("web_config")


app = Flask(__name__, template_folder="web//templates", static_folder="web//static")
app.register_blueprint(tool_blueprint)
# app.run()


if __name__ == '__main__':
    serve(app)
    pass