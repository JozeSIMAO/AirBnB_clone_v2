#!/usr/bin/python3
"""Starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


@app.route('/states', strict_slashes=False)
def list_states():
    """Displays a list of states"""
    states = storage.all(State).values()
    states_sorted = sorted(states, key=lambda x: x.name)

    return render_template('9-states.html', states=states_sorted)


@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """Displays cities of a state"""
    state = storage.get(State, id)
    if state:
        return render_template('9-states_cities.html', state=state)
    else:
        return render_template('9-not_found.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
