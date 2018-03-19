### Tours App
#
# App that will take input latitude & longitude output poi
# API's used Opensky & GooglePlaces
# Andrew, Patrick & Prince
# April 29th 2017
#
# Updated March 18th 2018 by Prince


import random
import math
import sys
from opensky_api import OpenSkyApi
from googleplaces import GooglePlaces, types, lang
from decimal import Decimal




def distance(lat1, lon1, lat2, lon2):
    R = 6731
    dLat = math.radians(lat2-lat1)
    dLon = math.radians(lon2-lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c



def getCompassDirection(heading):
    direction = ""
    if heading > 330 and heading < 30:
        direction = "N"
    elif heading > 30 and heading < 60:
        direction = "NE"
    elif heading > 60 and heading < 120:
        direction = "E"
    elif heading > 120 and heading < 150:
        direction = "SE"
    elif heading > 150 and heading < 210:
        direction = "S"
    elif heading > 210 and heading < 240:
        direction = "SW"
    elif heading > 240 and heading < 300:
        direction = "W"
    elif heading > 300 and heading < 330:
        direction = "NW"
        
    return direction




def main():
    while (True):
        #defining the api's used in the script
        google_places = GooglePlaces('AIzaSyBUzRTaHauZm8TPdV-1lqpoAjeE6vXd0hg')
        open_sky = OpenSkyApi()


        flights = open_sky.get_states()
        my_flight = {}


        #Lets user pick if they want to input a flight number or pick a random flight
        print("\n\nDo you want to input a flight number or pick a random flight?")
        print("1. Flight number")
        print("2. Random flight")
        ans = int(input("Answer (1 or 2): "))

        if ans == 1:
            callsign = input("\nWhat is your flight number? \n> ")

            flight_found = False
            for flight in flights.states:
                # get the dictornary of information held by the random flight
                # the call sign finds the unique airplane
                while(len(callsign) < 8):
                    callsign += ' '
              
                if callsign == flight.callsign:
                     my_flight = flight
                     flight_found = True
                     break

            if flight_found == False:      
                print ("Flight not found")
                main()
                sys.exit(0)

            
        elif ans == 2:
            #picks a random flight from the list of flight states
            randomNum = random.randrange(0,len(flights.states))
            callsign = flights.states[randomNum].callsign
            for flight in flights.states:
                # get the dictornary of information held by the random flight
                # the call sign finds the unique airplane
                if callsign == flight.callsign:
                     my_flight = flight
                     break


        else:
            print ("Invalid choice")
            main()
            sys.exit(0)




        # Print information about flight
        print("Callsign: \t\t\t" + my_flight.callsign)
        print("Altitude (meters): \t\t" + str(my_flight.baro_altitude))
        if my_flight.baro_altitude is not None: print("Altitude (feet): \t\t" + str(my_flight.baro_altitude // 0.3084))
        print("Velocity (m/s): \t\t" + str(my_flight.velocity))
        if my_flight.velocity is not None: print("Velocity (mph): \t\t" + str(my_flight.velocity * 2.23694))
        print("Heading (decimal degrees): \t" + getCompassDirection(my_flight.heading) + " (" + str(my_flight.heading) + ")")
        print("Country of origin: \t\t" + my_flight.origin_country) # Output the origin of the flight



        print("\n\nPlaces of interest near your flight:")
        # from our random flight use the lat and long from the open_air api in the google places api
        # using the lat and long we can find nearby points of interest to the airplane within a radius of 5km
        query_result = google_places.nearby_search(lat_lng={"lat": flight.latitude, "lng": flight.longitude}, type = "point_of_interest", radius=5000)
        for i in range(len(query_result.places)):
            # for the number of points outputed by google output those points
            place = query_result.places[i]
            print("%d: " % (i+1) + place.name)

        while (True):
            #  selecting one of the choices from above will prind out some information on that poi from the airplanes position
            choice = int(input("\nChoose a location to gain more information (0 to quit): "))
            if choice is 0:
                break;
            
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

            



main()
