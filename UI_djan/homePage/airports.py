import requests
class Airport:
    airportAPIKey = 'AIzaSyAu-knOMCv8nEGcTusCA9NOPo-Z7d0EwCs'
    nearAirport = 'http://maps.googleapis.com/maps/api/geocode/json?address=airport%20'
    airportDist = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='
    # ======================= A I R - P O R T - N E A R - B Y =====================================================

    def getAirAPIKey(self):
        return self.airportAPIKey

    def getDistToAirURL(self, latitude, longitude, airLat, airLon ):
        return self.airportDist + (str)(latitude) + ',' + (str)(longitude) + '&destinations=' + (str)(
            airLat) + ',' + (str)(airLon) + '&key=' + (str)(self.airportAPIKey)

    def getAirport(self, postCode, latitude, longitude):
        #global nearAirport, airportDist, airportAPIKey
        getNearAirPort = self.nearAirport + (str)(postCode) + '&sensor=false'
        getNearAirPort = requests.get(getNearAirPort)
        getNearAirPort = getNearAirPort.json()
        airportLat = getNearAirPort['results'][0]['geometry']['location']['lat']
        airportLon = getNearAirPort['results'][0]['geometry']['location']['lng']
        getDistanceToAirPort = Airport().getDistToAirURL(latitude, longitude, airportLat, airportLon)
        getDistanceToAirPort = requests.get(getDistanceToAirPort)
        getDistanceToAirPort = getDistanceToAirPort.json()
        name = getDistanceToAirPort['destination_addresses'][0]
        distance = getDistanceToAirPort['rows'][0]['elements'][0]['distance']['text']
        duration = getDistanceToAirPort['rows'][0]['elements'][0]['duration']['text']
        return name, distance, duration

