import requests
#import json
#-----------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------API HASH KEYS--------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#google geo api : AIzaSyBiUDxadU70wXZHE8e9dNYbdWmYSO4eHkI
#google place review api : AIzaSyDEfgx-keEaRVhYX6rPUNF8QwNBkpyVv_g
#google place reference:  AIzaSyBR9hsA0L7eNi5Nicgszt8eyvysLEL2mFo
distanceKey = '&key=AIzaSyCIvK5zFEQ0nJpv5EKWG1tAhBLU_52_wL0'
peopleReviewsKEY = 'AIzaSyBdGqqScqrz_KKxCPeTEjWOcxW5bbYYwXY'
googleGeoKey = '&key=AIzaSyBiUDxadU70wXZHE8e9dNYbdWmYSO4eHkI'
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------PARTS OF URLs FOR ACCESSING DATA----------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
geoURL = 'https://maps.googleapis.com/maps/api/geocode/json?address='
policeURL =  'https://data.police.uk/api/crimes-street/all-crime?'
distanceURL = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&'
hospitalsURL = 'https://data.gov.uk/data/api/service/health/hospitals/nearest?'
reviewsURL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
referenceURL = 'https://maps.googleapis.com/maps/api/place/details/json?reference='
#-----------------------------------------------------------------------------------------------------------------------
#-------------------------------------------PLACE RATINGS VARIABLE NAMES------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#rating_safety
#rating_health
#rating_people_review
#rating_education
#-----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------METHODS TO PARSE INPUT---------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
def printLine():    #print line for more readable output
    print('------------------------------------------------------------')

def parseDate(date):
    return date.replace('/', '-')

def parseAddress(address):
    return address.replace(' ', '+')
#-----------------------------------------------------------------------------------------------------------------------
#---------------------------------------METHODS TO CREATE URLs FOR ACCESSING DATA---------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
def getGeoURL(address):
    global geoURL, googleGeoKey
    address = parseAddress(address)
    totalGeoURL = geoURL + address + googleGeoKey  # total complete URL
    return totalGeoURL

def getPoliceURL(latitude, longitude):
    global policeURL
    totalPoliceURL = policeURL + 'lat=' + str(latitude) + '&lng=' + str(longitude)
    return totalPoliceURL

def getHospitalsURL(latitude, longitude):
    global hospitalsURL
    totalHospitalsURL = (str)(hospitalsURL) + 'lat=' + (str)(latitude)
    totalHospitalsURL = totalHospitalsURL + '&lon=' + (str)(longitude)
    return totalHospitalsURL

def getDistanceURL(origin_latitude, origin_longitude,
                   destination_latitude, destination_longitude):
    global distanceKey, distanceURL
    origin = 'origins=' + (str)(origin_latitude) + ',' + (str)(origin_longitude) + '&'
    destination = 'destinations=' + (str)(destination_latitude) + ',' + (str)(destination_longitude)
    totalDistanceURL = distanceURL + origin + destination + distanceKey
    return totalDistanceURL

def getReviewsURL(latitude, longitude):
    global reviewsURL, peopleReviewsKEY
    totalReviewsURL = reviewsURL + (str)(latitude) + ',' + (str)(longitude) + '&radius=500&key=' + peopleReviewsKEY
    return totalReviewsURL

#-----------------------------------------------------------------------------------------------------------------------
#---------------------------------------METHOD TO RETURN JSON FORMAT OF A REQUEST---------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
def getJsonRequest(someURL):
    getRequestResult = requests.get(someURL)
    getRequestResult = getRequestResult.json()
    return getRequestResult
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------METHOD TO RETURN COORDINATES FROM GEOLOCATION JSON----------------------------------
#-----------------------------------------------------------------------------------------------------------------------
def getCoordinatesGeoJson(jsonResult):
    location = jsonResult['results'][0]['geometry']['location']
    return location['lat'], location['lng']
#-----------------------------------------------------------------------------------------------------------------------
#----------------------------------------METHOD TO RETURN COORDINATES FROM GEO URL--------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
def getCoordinatesGeoURL(geoURL):
    jsonRequest = getJsonRequest(geoURL)
    lat, lng = getCoordinatesGeoJson(jsonRequest)
    return lat, lng
#-----------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------GETTING USER INPUT---------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
printLine()
printLine()
print('NOTE: If date field is ignored, the data')
print('\t  will be based on the most recent found.')
printLine()
printLine()
#date = input('Input the specific month and year YYYY/MM:')
#date = forDate(date)
#print(date)
userAddress = input('Enter your postcode or address seperated by commas: ')
#-----------------------------------------------------------------------------------------------------------------------
#----------------------------------------GETTING COORDINATES FOR USER GIVEN LOCATION------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
userLatitude, userLongitude = getCoordinatesGeoURL(getGeoURL(userAddress))
#-----------------------------------------------------------------------------------------------------------------------
#-------------------------------------------START COMPUTING CRIME STATS FOR AREA----------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#if(date is not ''):
#    total_CrimeURL = total_CrimeURL + '&date=' + str(date)
number_of_crimes = 0
crimes_array = []
crime_outcomes = []

policeJson = getJsonRequest(getPoliceURL(userLatitude, userLongitude))
#---------------------------------------------GET ALL CRIMES AND THEIR OUTCOMES-----------------------------------------
for crime in policeJson:
    crimes_array.append(policeJson[number_of_crimes]['category'])
    crime_outcomes.append(policeJson[number_of_crimes]['outcome_status'])
    number_of_crimes += 1
#-------------------------------------------COMPUTE THE NUMBER OF EACH CRIME TYPE---------------------------------------
category_counter = {}

for crime_category in crimes_array:
    if crime_category in category_counter:
        category_counter[crime_category] += 1
    else:
        category_counter[crime_category] = 1
#----------------------------------GET MOST COMMON CRIME AND HOW MANY TIMES IT WAS COMMITTED----------------------------
most_common_crime_number = 0
second_most_common_crime_number = 0
most_common_crime = ''
second_most_common_crime = ''
for category in category_counter:
    if(category_counter[category] > most_common_crime_number):
        second_most_common_crime = most_common_crime
        second_most_common_crime_number = most_common_crime_number

        most_common_crime_number = category_counter[category]
        most_common_crime = category

    elif(category_counter[category] > second_most_common_crime_number):
        second_most_common_crime_number = category_counter[category]
        second_most_common_crime = category

most_common_crime = most_common_crime.replace('-', ' ')
second_most_common_crime = second_most_common_crime.replace('-', ' ')
#---------------------------------GET NUMBER OF INVESTIGATIONS THAT FINISHED WITH NO SUSPECTS---------------------------
#-----------------------------------AND NUMBER OF CRIMES THAT ARE STILL UNDER INVESTIGATION-----------------------------
#---------------------------------------------------AND THEIR PERCENTAGE------------------------------------------------
no_suspects_found = 0
under_investigation = 0
number_of_crimes = len(crimes_array)

for outcome in crime_outcomes:
    if 'no suspect' in str(outcome):
        no_suspects_found += 1
    if 'Under investigation' in str(outcome):
        under_investigation += 1

ratio_unsolved_crimes = no_suspects_found / number_of_crimes * 100
ratio_investigating_crimes = under_investigation / number_of_crimes * 100
#--------------------------------------------GET THE PERCENTAGE OF SOLVED CRIMES----------------------------------------
ratio_solved_crimes = 100 - ratio_unsolved_crimes - ratio_investigating_crimes
#----------------------------------------COMPUTE THE SAFETY RATING FOR USER GIVEN AREA----------------------------------
rating_safety = int(ratio_solved_crimes)
rating_safety = rating_safety / 10
rating_safety = rating_safety + ratio_investigating_crimes / 100 - ratio_unsolved_crimes / 100
rating_safety = float(str('%.1f' % rating_safety))

if(rating_safety > 5):
    rating_safety = 5
if(rating_safety < 0):
    rating_safety = 0
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------PRINT SAFETY STATISTICS FOR USER GIVEN AREA-----------------------------------
#-----------------------------------------------------------------------------------------------------------------------
printLine()
printLine()
print('---------------YOUR SELECTED CRIME AREA STATS---------------')
printLine()
printLine()

if most_common_crime is not '':
    print('The total number of crimes around your given area is %s.\n' % number_of_crimes)
    if second_most_common_crime is not '':
        print('Most frequent crimes happening around your given area are %s ' % most_common_crime
                                                     + 'and %s.\n' % second_most_common_crime)
    else:
        print('The most frequent crime happening around your given area is %s.\n' % most_common_crime)

    print('Approximately %.0f%% of the total crimes around your given area have finished without finding any suspect.\n'
                                                                                           % ratio_unsolved_crimes)
    print('Approximately %.0f%% of the total crimes around your given area are still under investigation.\n'
                                                                                      % ratio_investigating_crimes)
else:
    print('No crimes could be found around your given location')
    rating_safety = 5
#-----------------------------------------------------------------------------------------------------------------------
#----------------------------------------START COMPUTING HEALTHCARE STATS FOR AREA--------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
hospitalJson = getJsonRequest(getHospitalsURL(userLatitude, userLongitude))

nearest_hospital_name = []

hospital_postcode_array = []
hospital_latitude_array = []
hospital_longitude_array = []
hospital_index = 0
#------------------------------------GETTING THE NAMES AND POSTCODES OF NEAREST HOSPITALS-------------------------------
hospitals_temporary_counter = 0
for hospital in hospitalJson['result'][hospital_index]:
     if(hospitals_temporary_counter == 3):
        break
     else:
         nearest_hospital_name.append(hospitalJson['result'][hospital_index]['name'])
         hospital_postcode_array.append(hospitalJson['result'][hospital_index]['postcode'])
         hospitals_temporary_counter += 1
         hospital_index += 1
#----------------------------------------COMPUTE COORDINATES FOR NEAREST HOSPITALS--------------------------------------
index = 0
for postcode in hospital_postcode_array:
    hospital_address = parseAddress(hospital_postcode_array[index])
    result_geo_json = getJsonRequest(getGeoURL(hospital_address))
    temp_location = result_geo_json['results'][0]['geometry']['location']
    hospital_latitude_array.append(temp_location['lat'])
    hospital_longitude_array.append(temp_location['lng'])
    index += 1
#------------------------------------------COMPUTE DISTANCES TO NEAREST HOSPITALS---------------------------------------
index = 0
hospitals_json = []
hospitals_distance = []
hospitals_distance_text = []

while (index < 3):
    hospitalDistanceURL = getDistanceURL(userLatitude, userLongitude,
                                         hospital_latitude_array[index], hospital_longitude_array[index])
    result_distance_json = getJsonRequest(hospitalDistanceURL)
    hospitals_json.append(result_distance_json)
    index += 1

index = 0
while (index < 3):
    hospitals_distance.append(hospitals_json[index]['rows'][0]['elements'][0]['distance']['value'])
    hospitals_distance_text.append(hospitals_json[index]['rows'][0]['elements'][0]['distance']['text'])
    index += 1
#-------------------------------------------COMPUTE NEAREST HOSPITAL INFORMATION----------------------------------------
nearest_index = 0
nearest_hospital_distance = hospitals_distance[0]

if(nearest_hospital_distance > hospitals_distance[1]):
    nearest_hospital_distance = hospitals_distance[1]
    nearest_index = 1

if(nearest_hospital_distance > hospitals_distance[2]):
    nearest_hospital_distance = hospitals_distance[2]
    nearest_index = 2

nearest_hospital_distance = nearest_hospital_distance / 1000
#-----------------------------------------------------------------------------------------------------------------------
#---------------------------------------PRINT HEALTHCARE STATISTICS FOR USER GIVEN AREA---------------------------------
#-----------------------------------------------------------------------------------------------------------------------
printLine()
printLine()
print('-------------YOUR SELECTED HEALTHCARE AREA STATS------------')
printLine()
printLine()
print('The nearest hospitals from your given area are :')
for hospital in nearest_hospital_name:
    print('\t*** %s ***' % hospital)

print('\nThe distance to the nearest hospital from your given area is %.2f kilometers.\n'
                                                                % nearest_hospital_distance)

average_distance = (hospitals_distance[0] + hospitals_distance[1] + hospitals_distance[2]) / 3000.0
print('The average distance between the nearest hospitals to your given area is %.2f kilometers.\n' % average_distance)

rating_health = 6 - (hospitals_distance[nearest_index] / 1000)
rating_health = rating_health - (average_distance / 10000)
rating_health = float(str('%.1f' % rating_health))

if(rating_health > 5):
    rating_health = 5
if(rating_health < 0):
    rating_health = 0
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------START COMPUTING REVIEWS STATS FOR AREA----------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
reviews_json = getJsonRequest(getReviewsURL(userLatitude, userLongitude))
#-------------------------------------------------GETTING ALL REVIEWS---------------------------------------------------
review_index = 0
reviews_array = []

for review in reviews_json['results']:
    if('rating' in reviews_json['results'][review_index]):
        reviews_array.append(reviews_json['results'][review_index]['rating'])
    review_index += 1
#-------------------------------------------COMPUTING THE AVERAGE OF ALL REVIEWS----------------------------------------
number_of_reviews = len(reviews_array)
sum_of_reviews = 0

for i in reviews_array:
    sum_of_reviews += i

average_review = sum_of_reviews / number_of_reviews
rating_people_review = float(str('%.1f' % average_review))
#-----------------------------------------------------------------------------------------------------------------------
#----------------------------------PRINT PEOPLE REVIEWS STATISTICS FOR USER GIVEN AREA----------------------------------
#-----------------------------------------------------------------------------------------------------------------------
printLine()
printLine()
print('---------------YOUR SELECTED AREA REVIEWS STATS-------------')
printLine()
printLine()
print('The total number of reviews collected from your given area is %i.' % number_of_reviews)
print('The average rating given by other people on the area is %.1f.\n' % rating_people_review)
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#----------------------------------------PRINT OVERALL RATINGS OF USER GIVEN AREA---------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
printLine()
printLine()
print('Safety Rating: \t\t%.1f/5.0' % rating_safety)
print('Healthcare Rating: \t%.1f/5.0' % rating_health)
print('Reviews Rating: \t%.1f/5.0' % rating_people_review)
print('-----------------\t-------')
rating_overall = (rating_safety + rating_health + rating_people_review) / 3
print('Overall Rating: \t%.1f/5.0' % rating_overall)
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------