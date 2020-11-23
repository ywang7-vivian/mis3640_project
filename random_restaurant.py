import csv
import urllib.request
import json
import urllib.request
import urllib.parse
import math
import random

MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MAPQUEST_MAP_URL = "https://www.mapquestapi.com/staticmap/v5/map"
MAPQUEST_API_KEY = "nd8A9WGP8NHkXh4RlGcCY33pQW7vhGkG"


def get_filename(dishType):
    filename = "Restaurants/Restaurants_" + dishType + ".csv"
    return filename


def read_csv(filename):
    """
    reads a csv file and returns a list
    """
    restaurants = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            restaurants.append(row)
        restaurants.pop(0)
    return restaurants


def get_distance(restuarant, user):
    """
    calculates distance (km) using two sets of latitude and longitude
    """
    lat1 = math.radians(restuarant[0])
    lon1 = math.radians(restuarant[1])
    lat2 = math.radians(user[0])
    lon2 = math.radians(user[1])
    dlon = lon1 - lon2
    dlat = lat1 - lat2
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon / 2) ** 2
    dist = 2 * math.asin(math.sqrt(a))*6371
    return dist


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)

    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding  API URL formatting requirements.
    """
    params = urllib.parse.urlencode(
        {'key': MAPQUEST_API_KEY, 'location': place_name})
    url = MAPQUEST_BASE_URL + "?" + params
    LatLng = get_json(url)["results"][0]["locations"][0]['displayLatLng']
    return LatLng['lat'], LatLng['lng']


def filter_distance(rest_list, user, dist=10):
    """
    filter the resturant based on the distance between the resturant and the user. Default distance is 10 km
    rest_dict1: resturant with value equals distance between the resturant and the user
    rest_dict2: resturant with value equals a list of information
    """
    user_location = get_lat_long(user)
    rest_dict1 = dict()
    rest_dict2 = dict()
    for restaurant in rest_list:
        rest_name = restaurant[0]
        rest_address = restaurant[2] + ', ' + \
            restaurant[3] + ', '+restaurant[4]
        rest_num = restaurant[5]
        rest_location = (float(restaurant[6]), float(restaurant[7]))
        rest_dist = get_distance(rest_location, user_location)
        if rest_dist < dist:
            if rest_name in rest_dict1:
                if rest_dist < rest_dict1[rest_name]:
                    rest_dict1[rest_name] = rest_dist
                    rest_dict2[rest_name] = (rest_address, rest_num,rest_location)
            else:
                rest_dict1[rest_name] = rest_dist
                rest_dict2[rest_name] = (rest_address, rest_num,rest_location)
    return rest_dict1, rest_dict2


def random_select(rest_dict):
    """
    Randomly selects one restaurant, returns name and address
    """
    rest_list = list(rest_dict)
    restaurant = random.choice(rest_list)
    info = rest_dict[restaurant]
    return restaurant, info


def random_restaurant(user, dishType="All", dist=10):
    """
    Takes in the location of the user, default distance is 10 km, and returns a random restaurant and address
    """
    filename = get_filename(dishType)
    rest_list = read_csv(filename)
    rest_dict = filter_distance(rest_list, user, dist=dist)[1]
    restaurant = random_select(rest_dict)
    return restaurant


def list_restaurant(user, dishType="All", dist=10):
    """
    Takes in the location of user, default distance is 10 km, and returns a list of all restaurants and their addresses
    """
    filename = get_filename(dishType)
    rest_list = read_csv(filename)
    distance = filter_distance(rest_list, user, dist=dist)[0]
    rest_dict = filter_distance(rest_list, user, dist=dist)[1]
    for rest in rest_dict:
        info = list(rest_dict[rest])
        dist = str(f"{distance[rest]:.2f}")
        info.append(dist)
        rest_dict[rest] = info
    return rest_dict


def get_map(user_location,restaurant_location,size):
    """
    Takes in user's location, restaurant(s)' location, and the specfied size, returns a list of locations
    user_location: latitude, longtitude
    restaurant_location: a list of latitude, longtitude
    """
    user = f"{user_location[0]},{user_location[1]}"

    restaurant=user+'|marker-start||'
    for locat in restaurant_location:
        restaurant+=f"{locat[0]},{locat[1]}|marker-{restaurant_location.index(locat)+1}||"
    restaurant = restaurant[:-2]

    mapSize = f"{size[0]},{size[1]}" 

    params = urllib.parse.urlencode(
        {'key':MAPQUEST_API_KEY, 'locations': restaurant,'size':mapSize})
    url = MAPQUEST_MAP_URL + "?" + params
    
    return url
    


def main():
    # print(random_restaurant('Jamaica Plain, MA, 02130', "American"))
    # print(read_csv(get_filename("American")))
    # print(list_restaurant('Jamaica Plain, MA, 02130', "American")['Common Ground'])
    # print(get_map((42.3097, -71.120796),[get_lat_long("150 Broadway, Chelsea, MA")],(1100,500)))
    print(get_distance((42.129046, -71.1015596),(42.310135, -71.113238)))



if __name__ == "__main__":
    main()
