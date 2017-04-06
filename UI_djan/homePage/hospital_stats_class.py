import requests
class HealthStats:

#=======================================================================================================================
    def __new__(cls):
        return super(HealthStats, cls).__new__(cls)
#=======================================================================================================================
    def __init__(self):
        self.hospitalsURL = 'https://data.gov.uk/data/api/service/health/hospitals/nearest?'
        self.rating_health = 0
        self.nearest_hospital_name = []
        self.hospital_postcode_array = []
        self.hospital_latitude_array = []
        self.hospital_longitude_array = []
        self.hospitals_json = []
        self.hospitals_distance = []
        self.hospitals_distance_text = []
        self.geoURL = 'https://maps.googleapis.com/maps/api/geocode/json?address='
        self.googleGeoKey = '&key=AIzaSyBiUDxadU70wXZHE8e9dNYbdWmYSO4eHkI'
        self.distanceURL = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&'
        self.distanceKey = '&key=AIzaSyCIvK5zFEQ0nJpv5EKWG1tAhBLU_52_wL0'
        self.nearest_index = 0
        self.nearest_hospital_distance = 0
        self.average_distance = 0
#=======================================================================================================================
    def parseAddress(self, address):
        return address.replace(' ', '+')
#=======================================================================================================================
    def getJsonRequest(self, someURL):
        getRequestResult = requests.get(someURL)
        getRequestResult = getRequestResult.json()
        return getRequestResult
#=======================================================================================================================
    def getGeoURL(self, address):
        address = self.parseAddress(address)
        totalGeoURL = self.geoURL + address + self.googleGeoKey  # total complete URL
        return totalGeoURL
#=======================================================================================================================
    def getDistanceURL(self, origin_latitude, origin_longitude,
                       destination_latitude, destination_longitude):
        origin = 'origins=' + (str)(origin_latitude) + ',' + (str)(origin_longitude) + '&'
        destination = 'destinations=' + (str)(destination_latitude) + ',' + (str)(destination_longitude)
        totalDistanceURL = self.distanceURL + origin + destination + self.distanceKey
        return totalDistanceURL
#=======================================================================================================================
    def getHospitalsURL(self, latitude, longitude):
        totalHospitalsURL = (str)(self.hospitalsURL) + 'lat=' + (str)(latitude)
        totalHospitalsURL = totalHospitalsURL + '&lon=' + (str)(longitude)
        return totalHospitalsURL
#=======================================================================================================================
    def computeNearestHospitalsInfo(self, hospitalJson):
        hospital_index = 0
        hospitals_temporary_counter = 0
        for hospital in hospitalJson['result'][hospital_index]:
            if (hospitals_temporary_counter == 3):
                break
            else:
                self.nearest_hospital_name.append(hospitalJson['result'][hospital_index]['name'])
                self.hospital_postcode_array.append(hospitalJson['result'][hospital_index]['postcode'])
                hospitals_temporary_counter += 1
                hospital_index += 1
#=======================================================================================================================
    def computeNearestHospitalsCoordinates(self):
        index = 0
        for postcode in self.hospital_postcode_array:
            hospital_address = self.parseAddress(self.hospital_postcode_array[index])
            result_geo_json = self.getJsonRequest(self.getGeoURL(hospital_address))
            temp_location = result_geo_json['results'][0]['geometry']['location']
            self.hospital_latitude_array.append(temp_location['lat'])
            self.hospital_longitude_array.append(temp_location['lng'])
            index += 1
#=======================================================================================================================
    def computeNearestHospitalsDistances(self, userLatitude, userLongitude):
        index = 0

        while (index < 3):
            hospitalDistanceURL = self.getDistanceURL(userLatitude, userLongitude,
                                      self.hospital_latitude_array[index], self.hospital_longitude_array[index])
            result_distance_json = self.getJsonRequest(hospitalDistanceURL)
            self.hospitals_json.append(result_distance_json)
            index += 1

        index = 0
        while (index < 3):
            self.hospitals_distance.append(self.hospitals_json[index]['rows'][0]['elements'][0]['distance']['value'])
            self.hospitals_distance_text.append(self.hospitals_json[index]['rows'][0]['elements'][0]['distance']['text'])
            index += 1
#=======================================================================================================================
    def computeInfoOfNearestHospital(self):
        self.nearest_index = 0
        self.nearest_hospital_distance = self.hospitals_distance[0]

        if (self.nearest_hospital_distance > self.hospitals_distance[1]):
            self.nearest_hospital_distance = self.hospitals_distance[1]
            nearest_index = 1

        if (self.nearest_hospital_distance > self.hospitals_distance[2]):
            self.nearest_hospital_distance = self.hospitals_distance[2]
            nearest_index = 2

        self.nearest_hospital_distance = self.nearest_hospital_distance / 1000
#=======================================================================================================================
    def computeHealthcareRating(self):
        self.average_distance = self.hospitals_distance[0] + self.hospitals_distance[1] + self.hospitals_distance[2]
        self.average_distance = self.average_distance / 3000.0
        self.rating_health = 6 - (self.hospitals_distance[self.nearest_index] / 1000)
        self.rating_health = self.rating_health - (self.average_distance / 10000)
        self.rating_health = float(str('%.1f' % self.rating_health))

        if (self.rating_health > 5):
            self.rating_health = 5
        if (self.rating_health < 0):
            self.rating_health = 0