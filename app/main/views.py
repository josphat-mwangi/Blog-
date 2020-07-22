from flask import Flask
from flask import render_template

@main.route("/")


posts = [
    {
        'author': 'jopa Mwas',
        'title': 'Blog Post 1',
        'content': 'First post content'
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'mwas jopa',
        'title': 'Blog Post 2',
        'content': 'second post content'
        'date_posted': 'April 21, 2018'
    }
]

@main.route("/home")
def home():
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
    retuen render_template('about.html', title='About')