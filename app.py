from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *
app = Flask(__name__)

app.config['SECRET_KEY'] = "newKey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route("/")
def render_home():
    """Show user the survey title and instructions with a start button"""
    return render_template("home.html", surveys=surveys)


@app.route("/instructions")
def show_instructions():
    survey_choice = request.args.get("survey_title")
    session["survey_choice"] = survey_choice
    survey = surveys[survey_choice]
    return render_template("instructions.html", survey=survey)


@app.route("/start", methods=["POST"])
def start_survey():
    """Redirect user to first question and clear session"""
    session["responses"] = []
    return redirect("/questions/0")


@app.route("/questions/<int:question_id>")
def show_question(question_id):
    """Show current question with choices"""
    responses = session.get("responses")
    survey_choice = session.get("survey_choice")
    survey = surveys[survey_choice]
    if (responses is None):
        return redirect("/")
    if (len(responses) >= len(survey.questions)):
        return redirect("/thanks")
    if (len(responses) != question_id):
        flash("Invalid question id", "invalid")
        return redirect(f"/questions/{len(responses)}")
    current_question = survey.questions[question_id]
    return render_template("question.html", survey=survey, question=current_question)


@app.route("/answer", methods=["POST"])
def handle_answer():
    """Add answer to response list and rediect to next question"""

    # ----> Is there a simpler solution for the following code? Why rebind?
    answer = request.form["answer"]
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    survey_choice = session.get("survey_choice")
    survey = surveys[survey_choice]
    if (len(responses) == len(survey.questions)):
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/thanks")
def render_thankyou():
    """Show thank you page when all questions are answered"""
    survey_choice = session.get("survey_choice")
    survey = surveys[survey_choice]
    return render_template("thanks.html", survey=survey)
