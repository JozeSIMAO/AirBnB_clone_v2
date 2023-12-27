#!/usr/bin/python3
"""
Script that starts a Flask web application
"""

from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Displays 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays 'HBNB'"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """Displays 'C ' followed by the value of the text variable"""
    return "C {}".format(escape(text.replace('_', ' ')))


@app.route('/python/<text>', strict_slashes=False)
def python_route(text="is cool"):
    """Displays 'Python ' followed by the value of the text variable"""
    return "Python {}".format(escape(text.replace('_', ' ')))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
