from flask import Flask
from flask import render_template,url_for,flash,redirect
from . import main

@main.route("/")



@main.route("/home")
def home():
    return render_template('home.html')

@main.route("/about")
def about():
    return render_template('about.html', title='About')