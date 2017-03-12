#google geo api : AIzaSyBiUDxadU70wXZHE8e9dNYbdWmYSO4eHkI
import requests
import json
distanceApi = '&key=AIzaSyCIvK5zFEQ0nJpv5EKWG1tAhBLU_52_wL0'
#-----------------------------------------------------------------------------------------------------------------------

geoURL = 'https://maps.googleapis.com/maps/api/geocode/json?address='
geoURL2 = '&key=AIzaSyBiUDxadU70wXZHE8e9dNYbdWmYSO4eHkI'
crime1 =  'https://data.police.uk/api/crimes-street/all-crime?'
distanceURL = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&'
hospitalsURL = 'https://data.gov.uk/data/api/service/health/hospitals/nearest?'

rating_safety = 0
rating_health = 0
rating_education = 0

#-----------------------------------------------------------------------------------------------------------------------

def forDate(date):     #this method used for the string date thingy.
    return date.replace('/', '-')

def forAddress(address):     #this one if for the address; changes the space to + so the url is complete.
    return address.replace(' ', '+')

def printLine():
    print('------------------------------------------------------------')
#-------------------------- M A I N - S T A R T S - H E R E ------------------------------------------------------------
printLine()
printLine()
print('NOTE: If date field is ignored, the data')
print('\t  will be based on the most recent found.')
printLine()
printLine()
date = input('Input the specific month and year YYYY/MM:')
date = forDate(date)
print(date)
address = input('Enter your address seperated by commas: ')
address = forAddress(address)
totalGeo = geoURL + address + geoURL2 #total complete URL
resultGeo = requests.get(totalGeo) #get the api request
resultGeo = resultGeo.json()
#print(resultGeo)
location = resultGeo['results'][0]['geometry']['location']
latitude, longitude = location['lat'], location['lng'] #got the latitude and longitude from geo api
#go the necessary info needed for the crime api. all ready to go now,yay!
#--------------------- C R I M E - A P I - S T A R T S - N O W ---------------------------------------------------------
total_CrimeURL =  str(crime1) + 'lat=' + str(latitude) + '&lng=' + str(longitude)
if(date is not ''):
    total_CrimeURL = total_CrimeURL + '&date=' + str(date)

result = requests.get(total_CrimeURL)
result = result.json()
crime_array = []
crime_outcomes = []

k = 0
for i in result:
    crime_array.append(result[k]['category'])
    crime_outcomes.append(result[k]['outcome_status'])
    k += 1
#-----------------------------------------------------------------------------------------------------------------------
# k = 0            # array A CONTAINS ALL THE TYPES OF CRIMES IN THAT AREA. TESTED AND IT WORKS
# for e in a:
#     print((a[k]))
#     k += 1
#     print('\n')
#-----------------------------------------------------------------------------------------------------------------------
category_counter = {}

for crime_category in crime_array:
    if crime_category in category_counter:
        category_counter[crime_category] += 1
    else:
        category_counter[crime_category] = 1

highest_crime_no = 0
highestCrime = ''
for category in category_counter:
    if(category_counter[category] > highest_crime_no):
        highest_crime_no = category_counter[category]
        highestCrime = category

no_suspects = 0
under_investigation = 0
solved_crimes = 0
for outcome in crime_outcomes:
    if 'no suspect' in str(outcome):
        no_suspects += 1
    if 'Under investigation' in str(outcome):
        under_investigation += 1
#------------------- P R I N T - T H E - S T A T S ---------------------------------------------------------------------
printLine()
printLine()
print('---------------YOUR SELECTED CRIME AREA STATS---------------')
printLine()
printLine()
if highestCrime is not '':
    print('The total number of crimes in given area is %s.\n' % len(crime_array))
    print('The most frequest crime happening in your area is %s.\n' % highestCrime)
    #compute useful information
    ratio_unsolved = no_suspects / len(crime_array) * 100
    ratio_investigating = under_investigation / len(crime_array) * 100
    solved_crimes = 100 - ratio_unsolved - ratio_investigating
    rating_safety = int(solved_crimes)
    rating_safety = float(rating_safety) / 10
    #print(rating_safety)
    if(rating_safety > 5):
        rating_safety = 5
    if(rating_safety < 0):
        rating_safety = 0
    ###########################
    print('%.2f%%' % ratio_unsolved + ' of the total crimes finished without finding any suspect.\n')
    print('%.2f%%' % ratio_investigating, ' of the total crimes are still under investigation.')
else:
    print('No crimes could be found at given location')
    rating_safety = 5
#===================================== C R I M E - S T A T S - O V E R =================================================
#=====================================HEALTH INFO STARTING==============================================================
printLine()
printLine()
print('-------------YOUR SELECTED HEALTHCARE AREA STATS------------')
printLine()
printLine()

hospitalGet = requests.get((str)(hospitalsURL) + 'lat=' + (str)(latitude) + '&lon=' + (str)(longitude))
hospitalGet = hospitalGet.json()

arrayPostCode = []
arrayLat = []
arrayLon = []
hosIndex = 0
tempIndex = 0

print('The closest hospitals near the given address are :')
for i1 in hospitalGet['result'][hosIndex]:
     if(tempIndex == 3):
        break
     else:
         print('\t\t',hospitalGet['result'][hosIndex]['name'])
         arrayPostCode.append(hospitalGet['result'][hosIndex]['postcode'])
         tempIndex += 1
         hosIndex += 1

print()
#-----------------------------------------------------------------------------------------------------------------------
#got the nearest hospitals and the post code, now find the latitude and longitudes of them and store in array:
ind = 0
for i in arrayPostCode:
    address = forAddress(arrayPostCode[ind])
    totalGeo = geoURL + address + geoURL2  # total complete URL
    resultGeo = requests.get(totalGeo)  # get the api request
    resultGeo = resultGeo.json()
    temp = requests.get(geoURL + i + geoURL2)
    temp = temp.json()
    tempLocation = resultGeo['results'][0]['geometry']['location']
    arrayLat.append(tempLocation['lat'])
    arrayLon.append(tempLocation['lng'])
    ind += 1

index = 0
hospitals_json = []
hospitals_distance = []
hospitals_distance_text = []

while (index < 3):
    distance_origin = 'origins=' + (str)(latitude) + ',' + (str)(longitude) + '&'
    distance_destination = 'destinations=' + (str)(arrayLat[index]) + ',' + (str)(arrayLon[index]) + distanceApi
    totalDistance = distanceURL + distance_origin + distance_destination
    #print(totalDistance)
    resultDistance = requests.get(totalDistance) #get the api request
    resultDistance = resultDistance.json()
    hospitals_json.append(resultDistance)
    index += 1

#print(resultDistance)
index = 0
while (index < 3):
    hospitals_distance.append(hospitals_json[index]['rows'][0]['elements'][0]['distance']['value'])
    hospitals_distance_text.append(hospitals_json[index]['rows'][0]['elements'][0]['distance']['text'])

    index += 1

nearest_index = 0
nearest_hospital_distance = hospitals_distance[0]

if(nearest_hospital_distance > hospitals_distance[1]):
    nearest_hospital_distance = hospitals_distance[1]
    nearest_index = 1

if(nearest_hospital_distance > hospitals_distance[2]):
    nearest_hospital_distance = hospitals_distance[2]
    nearest_index = 2

print('The distance to the nearest hospital is %s.\n' % hospitals_distance_text[nearest_index])

average_distance = (hospitals_distance[0] + hospitals_distance[1] + hospitals_distance[2]) / 3.0
print('The average distance between the nearest three hospitals to the given location is %.2f meters.\n' % average_distance)

rating_health = 6 - (hospitals_distance[nearest_index] / 1000)
rating_health = rating_health - (average_distance / 10000)
#print(rating_health)
#===================================== HEALTH CARE - S T A T S - O V E R ===============================================