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
@app.route("/hello", methods=["GET", "POST"])
def hello():

    # Get all of the user info in the database, send it to our hello.html template.
    logins = db.execute("SELECT * FROM logins").fetchall()

    # Login
    if request.method == "GET":
        return "Please submit the form instead."
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
    return render_template("hello.html", name=name, password=password, logins=logins)

@app.route("/register", methods=["POST"])
def register():
    return render_template("register.html")