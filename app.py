import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///albums.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    albums = db.execute("SELECT Title, Artist FROM fantano JOIN metacritic ON fantano.Title = metacritic.Title WHERE fantano.Rating > 8 AND metacritic.Metacritic Critic Score > 80")
    
    for album in albums:
        title = lookup(album["Title"])
        album["Artist"]  = title["Artist"] 

    return render_template("index.html", albums=albums)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        name = request.form.get("name")
        artist = request.form.get("artist")
        year = request.form.get("year")
        db.execute("INSERT INTO albums (name, artist, year) VALUES(?, ?)", name, artist, year)
        return redirect("/")

    else:

        albums = db.execute("SELECT * FROM albums")
        return render_template("index.html", albums=albums)

@app.route("/myalbums")
@login_required
def myalbums():
    """Show history of transactions"""

    # store SQL line in a variable
    albums = db.execute(
        "SELECT * FROM transactions WHERE user_id = ?", session["user_id"])

    # make history.html
    return render_template("history.html", transactions=transactions)
