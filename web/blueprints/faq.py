from flask import Blueprint, render_template, request, redirect, flash

faq_blueprint = Blueprint('faq', __name__)


@faq_blueprint.route("/faq", methods=["GET"])
def faq_get():
    return render_template("faq.html")
