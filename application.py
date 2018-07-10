import os
import requests, json
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    # Get all of the user info in the database, send it to our index.html template.
    logins = db.execute("SELECT * FROM logins").fetchall()
    return render_template("index.html", logins=logins)

# Enter username and password
@app.route("/login", methods=["GET", "POST"])
def login():

    # Get all of the user info in the database, send it to our login.html template.
    logins = db.execute("SELECT * FROM logins").fetchall()

    # Get login information
    if request.method == "GET":
        return render_template("getrequest.html", message="Please submit the form instead.")
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

    # Make sure flight exists.
    #if db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).rowcount == 0:
    #    return render_template("error.html", message="No such flight with that id.")

    return render_template("login.html", name=name, password=password, logins=logins)

@app.route("/register", methods=["GET", "POST"])
def register():

    # Get all of the user info in the database, send it to our register.html template.
    logins = db.execute("SELECT * FROM logins").fetchall()

    # Get login information
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    # Get all of the user info in the database, send it to our register.html template.
    #logins = db.execute("SELECT * FROM logins").fetchall()

    db.execute("INSERT INTO logins (username, password, email) VALUES (:username, :password, :email)",
                {"username": username, "password": password, "email": email})

    # Add information to logins
    db.commit()
    return render_template("success.html")

@app.route("/weather", methods=["GET", "POST"])
def weather():
    weather = requests.get("https://api.darksky.net/forecast/03420c86c79252e3e562d60cb56d5b03/42.37,-71.11").json()
    print(weather["currently"])
    return render_template("weather.html", weather=weather)