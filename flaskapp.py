import os
import gc
from functools import wraps
from datetime import datetime, timedelta

from flask import Flask, url_for, render_template, request, flash, redirect, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from flask_mail import Mail, Message
from wtforms import Form, validators, BooleanField, TextField, PasswordField
from dbconnect import connection

from dashboard_content import dashboard

from passlib.hash import pbkdf2_sha256
from MySQLdb import escape_string
#from models import User
# from flask_sqlalchemy import SQLAlchemy

from form_template import RegisterationForm, ContactForm

EMAIL = "mmbusif@gmail.com"

mail = Mail()

app = Flask(__name__)

# database connection
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test1.db"  # I should change this path.
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:adonese12@server/db"
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     confirmed_on = db.Column(db.DateTime, default=False, nullable=False)
#     confirm = db.Column(db.Boolean, nullable=True, default=False)


#     def __init__(self, username, email):
#         self.username = username
#         self.email = email


#     def __repr__(self):
#         return '<User %r>' % self.username



app.secret_key = "development key"  #TODO change this key to a much stronger one.
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = EMAIL
app.config["MAIL_PASSWORD"] = "Adonese=1994"
mail.init_app(app)


# List of navbars elements go here. I think there should be a better way of doing this.
DASHBOARD_CONTENTS = dashboard()
navbar_elements = ["about", "blog", "contact", "dashboard"]

@app.route('/')
def index():
    return render_template("index.html", navbar_elements=navbar_elements, title="gndi: The Best Place to Waste Your Money!")

@app.route("/about")
def about():
    return render_template("about.html", navbar_elements=navbar_elements)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "POST":
        if not form.validate():
            flash("This field is required")
            return render_template("contact.html", navbar_elements=navbar_elements, form=form)
        else:
            message = Message(subject=form.subject.data, recipients=[EMAIL], sender=form.email.data,
                              body=form.message.data)
            mail.send(message)
            return "Form Posted."
    elif request.method == "GET":
        return render_template("contact.html", navbar_elements=navbar_elements, form=form)

# TODO a message decorator.


@app.route("/blog")
def blog():
    return render_template("blog.html", navbar_elements=navbar_elements)


@app.route("/dashboard")
def dashboard():
    tabs_elements = ["GIS", "DATA ANALYSIS", "SCIENTIFIC COMPUTING", "ANDROID"]
    try:
        try:
            client_name, settings, tracking, rank = user_info()
            if len(tracking) < 10:
                # If he has only watched/read less than 10 topics.
                tracking = "/intro-to-programming"
            gc.collect()
            if client_name == "Guest":
                flash("Welcome Guest. Feel free to browse the contents. Progress tracking is only available for registered users.", "warning")
                tracking = ["None"]
            update_user_tracking()

            completed_percentage = topic_completion_percent()
            return render_template("dashboard.html", navbar_elements=navbar_elements, contents=DASHBOARD_CONTENTS, courses_list=list(DASHBOARD_CONTENTS.keys()), tabs=tabs_elements, completed_percentage=completed_percentage)
        except Exception as e:
            pass

    except Exception as e:
        pass

@app.route("/gis")
def gis_page():
    try:
        try:
            client_name, settings, tracking, rank = user_info()
            if len(tracking) < 10:
                # If he has only watched/read less than 10 topics.
                tracking = "/intro-to-programming"
            gc.collect()
            if client_name == "Guest":
                flash("Welcome Guest. Feel free to browse the contents. Progress tracking is only available for registered users.")
                tracking = ["None"]
            update_user_tracking()

            completed_percentage = topic_completion_percent()
            return render_template("gis.html", contents=DASHBOARD_CONTENTS, courses_list=list(DASHBOARD_CONTENTS.keys()), completed_percentage=completed_percentage)
        except Exception as e:
            pass

    except Exception as e:
        pass

@app.route("/login", methods=["GET", "POST"])
def login():
    
    try:
        c, conn = connection()
        error = None
        if request.method == "POST":
            data = c.execute("select * from users where username = (%s)", [escape_string(request.form["username"])])
            data = c.fetchone()[2]

            if pbkdf2_sha256.verify(request.form["password"], data):
                flash("You are Logged in.", "success")
                session["logged_in"] = True
                session["username"] = request.form["username"]
                # for keeping track of the users and admins.
                # session["rank"] = 2
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid credentials. Try again."
        gc.collect()
        return render_template("login.html", error=error)

    except Exception as e:
        error = "Invalid credentials. Try again."
        return render_template("login.html", error=error)

    return render_template("login.html", error=error)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first.")
            return redirect(url_for("login"))
    return wrap

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session.clear()
    flash("You have logged out.")
    gc.collect()
    return redirect(url_for("index"))


@app.route("/register", methods=["POST", "GET"])
def register():
    try:
        form = RegisterationForm(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = pbkdf2_sha256.encrypt(str(form.password.data))
            c, conn = connection()

            x = c.execute("select * from users where username = (%s)", [escape_string(username)])
            print("I'm in the first try.")
            if int(x) > 0:
                print("That is goood. It knows the username")
                flash("This username is already taken.")
                return render_template("register.html", form=form)

            else:
                c.execute("insert into users (username, password, email, tracking) values (%s, %s, %s, %s)", (escape_string(username), escape_string(password), escape_string(email), escape_string("/intro-to-programming")))
                conn.commit()
                print("I should be registered now.")
                flash("Thanks for registering.", "success")

                c.close()
                conn.close()
                gc.collect() # Garbage collection.

                session["logged_in"] = True
                session["username"] = username

                return redirect(url_for("dashboard"))

        gc.collect()
            
        return render_template("register.html", form=form)

                
    except Exception as e:
        return "An Exception has occured in Register template" + " " + str(e)

# Dashboard contents.

def user_info():
    try:
        client_name = session["username"]
        guest = False
    except:
        guest = True
        client_name = "Guest"
    if not guest:
        try:
            #user = User()
            #user_one = user.query.filter_by(username=session["username"]).first()

            c, conn = connection()
            c.execute("select * from users where username = (%s)", [(escape_string(client_name))])
            data = c.fetchone()
            print(data) # for debugging purposes.
            settings = data[4]
            tracking = data[5]
            rank = data[6]
        except Exception as e:
            pass
    else:
        settings = [0, 0]
        tracking = [0, 0]
        rank = [0, 0]

    return client_name, settings, tracking, rank


def update_user_tracking():
    try:
        completed = str(request.args["completed"])
        if completed in str(DASHBOARD_CONTENTS.values()):
            client_name, settings, tracking, rank = user_info()

            if tracking == None:
                tracking = completed
            else:
                if completed not in tracking:
                    tracking = tracking + "," + completed

            c, conn = connection()
            c.execute("update users set tracking = %s where username = %s", (escape_string(tracking), escape_string(client_name)))
            conn.commit()
            c.close()
            conn.close()

            #gc.collect()
            client_name, settings, tracking, ranking = user_info()

        else:
            pass

    except Exception as e:
        pass


def topic_completion_percent():
    try:

        client_name, settings, tracking, rank = user_info()

        try:
            tracking = tracking.split(",")
        except:
            pass
        
        if tracking == None:
            tracking = [] # The client doesn't completed any topic.
        completed_percentage = {}

        for category in DASHBOARD_CONTENTS:
            total, total_complete = 0, 0

            for topic in DASHBOARD_CONTENTS[category]:
                total += 1
                for completed_topic in tracking:
                    if completed_topic == topic[1]:
                        total_complete += 1

            percentage = (total_complete // total) * 100
            completed_percentage[category] = percentage

        return completed_percentage
    except:
        for category in DASHBOARD_CONTENTS:
            total, total_complete = 0, 0

            completed_percentage[category] = 0
        return completed_percentage
       
      

@app.errorhandler(404)
def page_not_found(e):
    try:
        gc.collect()
        rule = request.path

        if str(rule) in ["feed", "favicon", "wp-content", "wp-login", "wp-logout"]:
            pass
        else:
            error_logging = open("/var/www/gndi/website/four_for", "a")
            error_logging.write(str(rule)+"\n")
            return render_template("404.html"), 404

    except Exception as e:
        pass


@app.route("/sitemap.xml", methods=["GET"])
def sitemap():
    try:
        pages = []
        ten_days_ago = (datetime.now() - timedelta(days=7)).date().isoformat()

        for rule in app.url_map.iter_rules():
            if "GET" in rule.methods and len(rule.arguments) == 0:
                pages.append("http://gndi.com" + str(rule.rule), ten_days_ago)

        sitemap_xml = render_template("sitemap_template.xml", pages=pages)
        response = make_response(sitemap_xml)
        response.headers["Content-Type"] = "applications/xml"
        return response

    except Exception as e:
        pass

@app.route("/robots.txt")
def robots():
    return "User-agent: * \nDisallow: /register\n Disallow: /login\n Disallow: /logout"

if __name__ == '__main__':
    app.run(debug=True)
