import requests
import urllib.request
import json

geoURL = 'https://maps.googleapis.com/maps/api/geocode/json?address='
geoURL2 = '&key=AIzaSyBiUDxadU70wXZHE8e9dNYbdWmYSO4eHkI'
hospitalsURL = 'https://data.gov.uk/data/api/service/health/hospitals/nearest?'

def forAddress(address):     #this one if for the address; changes the space to + so the url is complete.
    return address.replace(' ', '+')

address = input('Enter your address seperated by comas: ')
address = forAddress(address)
totalGeo = geoURL + address + geoURL2 #total complete URL
resultGeo = requests.get(totalGeo) #get the api request
resultGeo = resultGeo.json()
location = resultGeo['results'][0]['geometry']['location']
latitude, longitude = location['lat'], location['lng'] #got the latitude and longitude from geo api

print(latitude, longitude)

hospitalGet = requests.get((str)(hospitalsURL) + 'lat=' + (str)(latitude) + '&lon=' + (str)(longitude))
hospitalGet = hospitalGet.json()
print(hospitalGet)
arrayPostCode = []
arrayLat = []
arrayLon = []
hosIndex = 0
tempIndex = 0
length = len(hospitalGet['result'][0])
print('Total hospitals near you are :', length)
print('The closest hospitals near you are :')
for i in hospitalGet['result'][hosIndex]:
     if(tempIndex == 3):
        break
     else:
         print('\t\t',hospitalGet['result'][hosIndex]['name'])
         arrayPostCode.append(hospitalGet['result'][hosIndex]['postcode'])
         tempIndex += 1
         hosIndex += 1

print(arrayPostCode)
#-----------------------------------------------------------------------------------------------------------------------
#got the nearest hospitals and the post code, now find the latitude and longitudes of them and store in array:
for i in arrayPostCode:
    temp = requests.get(geoURL + i + geoURL2)
    temp = temp.json()
    tempLocation = resultGeo['results'][0]['geometry']['location']
    arrayLat.append(tempLocation['lat'])
    arrayLon.append(tempLocation['lng'])
print(arrayLat)
print(arrayLon)
#-----------------------------------------------------------------------------------------------------------------------