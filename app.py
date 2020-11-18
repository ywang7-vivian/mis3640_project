"""
Simple "Hello, World" application using Flask
"""

from flask import Flask, request, render_template, redirect, url_for, session
from random_restaurant import random_restaurant as random_rest
from random_restaurant import list_restaurant
import random

app = Flask(__name__)

app.secret_key = 'ilovepython'

typeList = ['American', 'Asian_Fusion', 'Barbeque', 'Breakfast', 'Burger', 'Cajun', 'Caribbean', 'Chicken_and_Wings', 'Chinese', 'Drive_In', 'Ethnic', 'Family', 'Fast_Food', 'Food_Delivery', 'French', 'German', 'Gluten_Free', 'Greek', 'Hawaiian',
                                                'Healthy', 'Hot_Dogs', 'Indian_Pakistan', 'Italian', 'Japanese', 'Korean', 'Latin_American', 'Lebanese', 'Meditteranean', 'Mexican', 'Seafood', 'Soup', 'Southern', 'Spanish', 'Tex-Mex', 'Thai', 'Vegan', 'Vegitarian', 'Vietnamese', 'Middle_Eastern']

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/random', methods=['POST'])
def random_restaurant():
    if request.method == 'POST':
        user_location = request.form['user_location']
        session['user_location'] = user_location
        distance = float(request.form['distance'])
        session['distance'] = distance
        dishType = request.form['dishType']
        session['dishType'] = dishType
        
        if not user_location:
            return render_template('index.html', error=True)

        if request.form['choice'] == "list":
            return redirect(url_for('result2'))
        
        return redirect(url_for('result'))


@app.route('/random_restaurant', methods=['GET', 'POST'])
def result():
    if request.method == 'GET':
        user_location = session.get('user_location',None)
        distance = session.get('distance',None)
        dishType = session.get('dishType')
        if dishType == "All":
            while True:
                try:
                    # dishType = random.choice(typeList)
                    dishType = 'American'
                    restaurant = random_rest(user_location, dishType, distance)
                    break
                except:
                    pass

        try:
            restaurant = random_rest(user_location, dishType, distance)
        except IndexError:
            return render_template('restaurant_error.html')
        rest_name = restaurant[0]
        rest_add = restaurant[1][0]
        rest_num = restaurant[1][1]
        dishType = session.get('dishType', None)
        
        return render_template('restaurant_result.html', rest_name=rest_name, rest_add=rest_add, rest_num=rest_num, dish_type=dishType)


@app.route('/list_restaurant', methods=['GET', 'POST'])
def result2():
    if request.method == 'GET':
        user_location = session.get('user_location',None)
        distance = session.get('distance',None)
        dishType = session.get('dishType')
        if dishType != "All":
            listRest = list_restaurant(user_location, dishType, distance)
            for rest in listRest:
                listRest[rest].append(dishType)

        else:
            dictRest = dict()
            for dish_Type in typeList:
                dictRest[dish_Type] = list_restaurant(user_location, dish_Type, distance)
            listRest = dict()
            for rest_Type in dictRest:
                for restaurant in dictRest[rest_Type]:
                    dictRest[rest_Type][restaurant].append(rest_Type)
                    listRest[restaurant] = dictRest[rest_Type][restaurant]
        
        listRestau = list(listRest.items())
        listRestau = sorted(listRestau, key = lambda x: x[1][2])

        return render_template('restaurant_list.html',len = len(listRestau),listRest=listRestau)
