### Tours App
#
# App that will take input latitude & longitude output poi
# API's used Opensky & GooglePlaces
# Andrew, Patrick & Prince
# April 29th 2017


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

#defining the api's used in the script
google_places = GooglePlaces('AIzaSyBUzRTaHauZm8TPdV-1lqpoAjeE6vXd0hg')
open_sky = OpenSkyApi()

#flight_number =  raw_input("What is your flight number? \n> ")
flights = open_sky.get_states()

#picks a random flight from the list of flight states
random = random.randrange(0,len(flights.states))
callsign = flights.states[random].callsign

# defines my_flight as the randomly picked flight
my_flight = {}
for flight in flights.states:
    # get the dictornary of information held by the random flight
    # the call sign finds the unique airplane
    if callsign == flight.callsign:
   	 my_flight = flight
   	 # output the origin of the flight
   	 print("Country of origin: " + my_flight.origin_country)
   	 break

# from our random flight use the lat and long from the open_air api in the google places api
# using the lat and long we can find nearby points of interest to the airplane within a radius of 5km
query_result = google_places.nearby_search(lat_lng={"lat": flight.latitude, "lng": flight.longitude}, type = "point_of_interest", radius=5000)
for i in range(len(query_result.places)):
    # for the number of points outputed by google output those points
    place = query_result.places[i]
    print("%d: " % (i+1) + place.name)

while (True):
    #  selecting one of the choices from above will prind out some information on that poi from the airplanes position
    choice = input("Choose a location to gain more information: ")
    place = query_result.places[choice-1]
    # this spits out a dictionary of information about the point
    place.get_details()
    # get lat and long of the poi
    lat = float(place.geo_location["lat"])
    lng = float(place.geo_location["lng"])
    # use the distance functin to find the position from the airplane to the poi
    d = distance(my_flight.latitude, my_flight.longitude, lat, lng)
	
	# these calculations find the position of the poi relative to the airplane
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
