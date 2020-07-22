from flask import Flask
from flask import render_template

@main.route("/")

@main.route("/home")
def home():
    return render_template('home.html')

@main.route("/about")
def about():
    retuen render_template('about.html')