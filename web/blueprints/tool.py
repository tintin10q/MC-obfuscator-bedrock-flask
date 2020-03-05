from flask import Blueprint, render_template, request

tool_blueprint = Blueprint('main', __name__)

@tool_blueprint.route("/", methods=["GET"])
def tool_post():
    print("cool")
    return render_template("tool.html")

@tool_blueprint.route("/", methods=["POST"])
def tool_get():
    print(request.form)
    return "post"