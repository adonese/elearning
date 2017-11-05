from flask import Blueprint, render_template, flash, redirect, url_for
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from .nav import nav

frontend = Blueprint('frontend', __name__)


@frontend.route("/")
def index():
    return render_template("index.html")


@frontend.route("/about-us")
def about():
    return render_template("about.html")
