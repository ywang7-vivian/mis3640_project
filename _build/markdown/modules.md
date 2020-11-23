# random_restaurant.py


### random_restaurant.filter_distance(rest_list, user, dist=10)
filter the resturant based on the distance between the resturant and the user. Default distance is 10 km
rest_dict1: resturant with value equals distance between the resturant and the user
rest_dict2: resturant with value equals a list of address, tel_number, and (latitude, longtitude)


### random_restaurant.get_distance(restuarant, user)
calculates distance (km) using two sets of latitude and longitude


### random_restaurant.get_json(url)
Given a properly formatted URL for a JSON web API request, return
a Python JSON object containing the response to that request.


### random_restaurant.get_lat_long(place_name)
Given a place name or address, return a (latitude, longitude) tuple
with the coordinates of the given place.
See [https://developer.mapquest.com/documentation/geocoding-api/address/get/](https://developer.mapquest.com/documentation/geocoding-api/address/get/)
for Mapquest Geocoding  API URL formatting requirements.


### random_restaurant.get_map(user_location, restaurant_location, size)
Takes in user’s location, restaurant(s)’ location, and the specfied size, returns a list of locations
user_location: latitude, longtitude
restaurant_location: a list of latitude, longtitude


### random_restaurant.list_restaurant(user, dishType='All', dist=10)
Takes in the location of user, default distance is 10 km, and returns a list of all restaurants and their addresses


### random_restaurant.random_restaurant(user, dishType='All', dist=10)
Takes in the location of the user, default distance is 10 km, and returns a random restaurant and address


### random_restaurant.random_select(rest_dict)
Randomly selects one restaurant, returns name and address


### random_restaurant.read_csv(filename)
reads a csv file and returns a list

# app.py

Simple “Hello, World” application using Flask


### app.hello()
Returns Home Page


### app.random_restaurant()
Gets user’s inputs, checks if the user has entered the location, and redirects based on user’s choice of “I am Lucky today” or “List all options”.


### app.result()
Returns the result page of “I am lucky today” or redirects to error page if there is no restaurant nearby


### app.result2()
Returns the result page of “List all options”.
