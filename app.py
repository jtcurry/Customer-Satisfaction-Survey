from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *
app = Flask(__name__)

app.config['SECRET_KEY'] = "newKey"
debug = DebugToolbarExtension(app)


responses = []


@app.route("/")
def render_home():
    """Show user the survey title and instructions with a start button"""
    return render_template("home.html", survey=satisfaction_survey)
