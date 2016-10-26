"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Movie, Rating


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/users/<user_id>")
def show_user_page(user_id):
    """Show individual user's info"""

    user = User.query.get(user_id)
    ratings_list = db.session.query(Rating.score, Movie.title).join(Movie).filter(Rating.user_id==user_id).all()

    return render_template("user_page.html", user=user, ratings_list=ratings_list)


@app.route("/login")
def show_login():
    """Shows the log-in form"""


    return render_template("login_form.html")

@app.route("/login", methods=["POST"])
def login_process():
    """Processes the login information"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Email does not exist. Please try again or register.")
        return redirect("/login")
    elif user and (user.password == password):
        flash("Login Successful.")
        session['user_id'] = user.user_id
        return redirect("/")
    else:
        flash("Password incorrect. Please try again.")
        return redirect("/login")

@app.route("/logout")
def show_logout():
    """Shows the logout option"""

    flash("Logged out. Thanks for visiting Ratings!")
    del session['user_id']

    return redirect("/")

        

@app.route("/register")
def show_registration():
    """Shows the registration form"""


    return render_template("register_form.html")

@app.route("/register", methods=["POST"])
def registration_process():
    """Processes the registration information"""

    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

    user = User.query.filter_by(email=email).first()

    if user:
        flash("You're already in our system. Please login.")
        return redirect("/login")
    else:
        #send info to update User database
        user = User(email=email, password=password, age=int(age), zipcode=zipcode)
        db.session.add(user)
        db.session.commit()
        #redirect to home
        flash("Registration Successful. Welcome to Ratings!")
        return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run()
