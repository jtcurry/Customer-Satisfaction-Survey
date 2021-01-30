from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *
app = Flask(__name__)

app.config['SECRET_KEY'] = "newKey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


responses = []


@app.route("/")
def render_home():
    """Show user the survey title and instructions with a start button"""
    return render_template("home.html", survey=satisfaction_survey)

@app.route("/questions/<int:question_id>")
def show_question(question_id):
    """Show current question with choices"""
    survey=satisfaction_survey
    current_question = survey.questions[question_id]
    return render_template("question.html", survey = survey, question = current_question)

@app.route("/answer", methods=["POST"])
def handle_answer():
    """Add answer to response list and rediect to next question"""
    answer = request.form["answer"]
    responses.append(answer)
    return redirect(f"/questions/{len(responses)}")
    