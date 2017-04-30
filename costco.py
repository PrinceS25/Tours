### Tours App
#
# App that will take input latitude & longitude output poi
# API's used Opensky & GooglePlaces
# Opensky -> location and on-ground

from opensky_api import OpenSkyApi
from googleplaces import GooglePlaces, types, lang
import random
import math
from decimal import Decimal

def distance(lat1, lon1, lat2, lon2):
    R = 6731
    dLat = math.radians(lat2-lat1)
    dLon = math.radians(lon2-lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

print
google_places = GooglePlaces('AIzaSyBUzRTaHauZm8TPdV-1lqpoAjeE6vXd0hg')
open_sky = OpenSkyApi()

#flight_number =  raw_input("What is your flight number? \n> ")
flights = open_sky.get_states()

random = random.randrange(0,len(flights.states))
callsign = flights.states[random].callsign

my_flight = {}
for flight in flights.states:
    if callsign == flight.callsign:
   	 my_flight = flight
   	 print("Country of origin: " + my_flight.origin_country)
   	 break

query_result = google_places.nearby_search(lat_lng={"lat": flight.latitude, "lng": flight.longitude}, type = "point_of_interest", radius=5000)
for i in range(len(query_result.places)):
    place = query_result.places[i]
    print("%d: " % (i+1) + place.name)

while (True):
    print
    choice = input("Choose a location to gain more information: ")
    place = query_result.places[choice-1]
    place.get_details()
    lat = float(place.geo_location["lat"])
    lng = float(place.geo_location["lng"])
    d = distance(my_flight.latitude, my_flight.longitude, lat, lng)

    NS_direction = "N"
    WE_direction = "W"
    netLat = my_flight.latitude - lat
    netLng = my_flight.longitude - lng
    if netLat > 0:
        NS_direction = "S"
    if netLng > 0:
        WE_direction = "E"
        
    
    print("Distance: %.2f km" % d)
    print("Direction: " + NS_direction + WE_direction)
    #print(query_result.places[choice-1].details)
