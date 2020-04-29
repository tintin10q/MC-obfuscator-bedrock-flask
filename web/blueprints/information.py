from flask import Blueprint, render_template, request, redirect, flash

information_blueprint = Blueprint('information', __name__)


@information_blueprint.route("/information", methods=["GET"])
def information_get():
    return render_template("information.html")
