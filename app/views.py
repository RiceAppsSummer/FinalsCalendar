from flask import render_template

from app import app

@app.route('/')
def test():
    return render_template("layout.html")
