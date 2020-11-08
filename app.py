"""
Simple "Hello, World" application using Flask
"""

from flask import Flask, request, render_template, redirect, url_for, session
from random_restaurant import random_restaurant as random_rest
import random

app = Flask(__name__)

app.secret_key = 'ilovepython'


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/nearest', methods=['POST'])
def random_restaurant():
    if request.method == 'POST':
        user_location = request.form['user_location']
        distance = float(request.form['distance'])
        dishType = request.form['dishType']
        session['dishType'] = dishType

        if not user_location:
            return render_template('index.html', error=True)

        if dishType == "All":
            while True:
                try:
                    dishType = random.choice(['American', 'Asian_Fusion', 'Barbeque', 'Breakfast', 'Burger', 'Cajun', 'Caribbean', 'Chicken_and_Wings', 'Chinese', 'Drive_In', 'Ethnic', 'Family', 'Fast_Food', 'Food_Delivery', 'French', 'German', 'Gluten_Free', 'Greek', 'Hawaiian',
                                              'Healthy', 'Hot_Dogs', 'Indian_Pakistan', 'Italian', 'Japanese', 'Korean', 'Latin_American', 'Lebanese', 'Meditteranean', 'Mexican', 'Seafood', 'Soup', 'Southern', 'Spanish', 'Tex-Mex', 'Thai', 'Vegan', 'Vegitarian', 'Vietnamese', 'Middle_Eastern'])
                    session['dishType'] = dishType
                    restaurant = random_rest(user_location, dishType, distance)
                    session['restaurant'] = restaurant
                    return redirect(url_for('result'))
                except:
                    pass

        try:
            restaurant = random_rest(user_location, dishType, distance)
            session['restaurant'] = restaurant
            return redirect(url_for('result'))
        except IndexError:
            return render_template('restaurant_error.html')


@app.route('/nearest_restaurant', methods=['GET', 'POST'])
def result():
    if request.method == 'GET':
        restaurant = session.get('restaurant', None)
        rest_name = restaurant[0]
        rest_add = restaurant[1][0]
        rest_num = restaurant[1][1]
        dishType = session.get('dishType', None)
        return render_template('restaurant_result.html', rest_name=rest_name, rest_add=rest_add, rest_num=rest_num, dish_type=dishType)
