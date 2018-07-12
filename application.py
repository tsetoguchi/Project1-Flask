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

@app.route("/", methods=["GET", "POST"])
def index():

    # Get all of the user info in the database, send it to our index.html template.
    logins = db.execute("SELECT * FROM logins").fetchall()
    return render_template("index.html", logins=logins)

# Enter username and password
@app.route("/login", methods=["GET", "POST"])
def login():

    # Get all of the user info in the database, send it to the login.html template.
    logins = db.execute("SELECT * FROM logins").fetchall()

    # Get all of the zipcode information in the database, send it to the login.html template.
    zips = db.execute("SELECT * FROM zips").fetchall()


    # Get login information
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        # Query for username and password
        username = db.execute("SELECT username FROM logins where username = :username", {"username": name}).fetchone()
        password_ = db.execute("SELECT password FROM logins where password = :password", {"password": password}).fetchone()
        print(password_[0])
        print(request.form["password"])
        print(username[0])
        print(request.form["name"])
        if request.form["password"] == password_[0] and request.form["name"] == username[0]:
            session["user_id"] = id
            return render_template("login.html", name=name, password=password, logins=logins, zips=zips, id=session["user_id"])
        if username[0] or password_[0] == None:
            return render_template("invalidlogin.html")
        elif name == '' or password == '':
            return render_template("invalidlogin.html")


        # Check if username or password fields are empty

        # elif (request.form["password"] == password_[0] and request.form["name"] == username[0]) is False:
        #     return render_template("invalidlogin.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    return render_template("register.html")

@app.route("/success", methods=["GET", "POST"])
def success():

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

@app.route("/locations", methods=["GET", "POST"])
def locations():

    # Get all of the user info in the database, send it to our locations.html template.
    zips = db.execute("SELECT * FROM zips").fetchall()

    # Check if session is active
    if session["user_id"] == id:

        if request.method == "POST":
            # Get all of the zip info in the database, send it to our locations.html template.
            zips = db.execute("SELECT * FROM zips").fetchall()

            # Get zipcode or city
            zipcode = '%' + request.form.get("zipcode") + '%'
            # Similar zipcodes
            similar = db.execute("SELECT * FROM zips WHERE zipcode LIKE :zip", {"zip": zipcode}).fetchall()
            if similar == []:
                return render_template("invalidsearch.html")
            else:
                return render_template("locations.html", weather=weather, zips=zips, zipcode=zipcode, similar=similar)

    else:
        return render_template("unsuccessful.html")

@app.route("/location/<zipcode>")
def location(zipcode):


    # Make sure zipcode exists.
    zip = db.execute("SELECT * FROM zips WHERE zipcode = :zip", {"zip": zipcode}).fetchone()
    if zip is None:
        return render_template("invalidsearch.html")

    # Get weather
    weather = requests.get("https://api.darksky.net/forecast/03420c86c79252e3e562d60cb56d5b03/" + str(zip[3]) + "," + str(zip[4])).json()
    print('********************************')
    print("https://api.darksky.net/forecast/03420c86c79252e3e562d60cb56d5b03/" + str(zip[3]) + "," + str(zip[4]))
    # Similar zipcodes
    similar = db.execute("SELECT * FROM zips WHERE zipcode LIKE :zip", {"zip": zipcode}).fetchall()
    if similar == []:
        return render_template("invalidsearch.html")
    else:
        return render_template("location.html", zip=zip, similar=similar, weather=weather)




@app.route("/logout", methods=["GET", "POST"])
def logout():

    # Check if session is active
    if session["user_id"] == id:
        session.clear()
        return render_template("logout.html")
    else:
        return render_template("unsuccessful.html")

@app.route("/weather", methods=["GET", "POST"])
def weather():

    # Check if session is active
    if session["user_id"] == id:

        # Get all of the user info in the database, send it to our weather.html template.
        logins = db.execute("SELECT * FROM logins").fetchall()
        zipcode = request.form.get("zipcode")
        weather = requests.get("https://api.darksky.net/forecast/03420c86c79252e3e562d60cb56d5b03/%55.55,-70.77").json()
        return render_template("weather.html", weather=weather, zipcode=zipcode)

    else:
        return render_template("unsuccessful.html")

@app.route("/invalidsearch", methods=["GET", "POST"])
def invalidsearch():

    if session["user_id"] == id:
        return render_template("invalidsearch.html")
    else:
        return render_template("unsuccessful.html")