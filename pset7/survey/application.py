import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Feedback
feedbacks = []

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    name = request.form.get("name")
    meal = request.form.get("meal")
    stars = request.form.get("stars")
    if not name:
        return render_template("error.html", message="Please fill in missing fields")
    if not meal:
        return render_template("error.html", message="Please fill in missing fields")
    if not stars:
        return render_template("error.html", message="Please fill in missing fields")
    file = open("survey.csv", "a")
    writer = csv.writer(file)
    writer.writerow((request.form.get("name"), request.form.get("meal"), request.form.get("stars")))
    file.close()
    feedbacks.append(f"{name} rated {meal} {stars}")
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    return render_template("feedback.html", feedbacks=feedbacks)
    if len(feedbacks) == 0:
        return render_template("error.html", message="Empty")
