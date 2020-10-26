"""
Simple "Hello, World" application using Flask
"""

from flask import Flask
from flask import request
from flask import render_template
from random_restaurant import random_restaurant as random

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def random_restaurant():
    if request.method == 'POST':
        user_location = request.form['user_location']
        distance = float(request.form['distance'])
        restaurant = random(user_location,distance)
        rest_name = restaurant[0]
        rest_add = restaurant[1]
        return render_template('restaurant_result.html',rest_name = rest_name, rest_add = rest_add)
    return render_template('index.html')


