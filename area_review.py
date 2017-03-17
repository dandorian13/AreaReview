from police_stats_class import *
from hospital_stats_class import *
from reviews_stats_class import *
import requests
#import json
#-----------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------API HASH KEYS--------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#google geo api : AIzaSyBiUDxadU70wXZHE8e9dNYbdWmYSO4eHkI
#google place reference:  AIzaSyBR9hsA0L7eNi5Nicgszt8eyvysLEL2mFo
googleGeoKey = '&key=AIzaSyBiUDxadU70wXZHE8e9dNYbdWmYSO4eHkI'
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------PARTS OF URLs FOR ACCESSING DATA----------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
geoURL = 'https://maps.googleapis.com/maps/api/geocode/json?address='
referenceURL = 'https://maps.googleapis.com/maps/api/place/details/json?reference='
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
police_stats = PoliceStats()
policeJson = police_stats.getJsonRequest(police_stats.getPoliceURL(userLatitude, userLongitude))
police_stats.computeCrimesStats(policeJson)
police_stats.countCrimeCategory()
police_stats.computeMostCommonCrimes()
police_stats.computeNumberOfCrimes()
police_stats.computeUnsolvedCrimes()
police_stats.computeCrimesRatios()
police_stats.computeSafetyRating()
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------PRINT SAFETY STATISTICS FOR USER GIVEN AREA-----------------------------------
#-----------------------------------------------------------------------------------------------------------------------
printLine()
printLine()
print('---------------YOUR SELECTED CRIME AREA STATS---------------')
printLine()
printLine()

if police_stats.most_common_crime is not '':
    print('The total number of crimes around your given area is %s.\n' % police_stats.number_of_crimes)
    if police_stats.second_most_common_crime is not '':
        print('Most frequent crimes happening around your given area are %s ' % police_stats.most_common_crime
                                                     + 'and %s.\n' % police_stats.second_most_common_crime)
    else:
        print('The most frequent crime happening around your given area is %s.\n' % police_stats.most_common_crime)

    print('Approximately %.0f%% of the total crimes around your given area have finished without finding any suspect.\n'
                                                                                           % police_stats.ratio_unsolved_crimes)
    print('Approximately %.0f%% of the total crimes around your given area are still under investigation.\n'
                                                                                      % police_stats.ratio_investigating_crimes)
else:
    print('No crimes could be found around your given location')
    rating_safety = 5
#-----------------------------------------------------------------------------------------------------------------------
#----------------------------------------START COMPUTING HEALTHCARE STATS FOR AREA--------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
hospitals_stats = HealthStats()
hospitalJson = hospitals_stats.getJsonRequest(hospitals_stats.getHospitalsURL(userLatitude, userLongitude))
hospitals_stats.computeNearestHospitalsInfo(hospitalJson)
hospitals_stats.computeNearestHospitalsCoordinates()
hospitals_stats.computeNearestHospitalsDistances(userLatitude, userLongitude)
hospitals_stats.computeInfoOfNearestHospital()
hospitals_stats.computeHealthcareRating()
#-----------------------------------------------------------------------------------------------------------------------
#---------------------------------------PRINT HEALTHCARE STATISTICS FOR USER GIVEN AREA---------------------------------
#-----------------------------------------------------------------------------------------------------------------------
printLine()
printLine()
print('-------------YOUR SELECTED HEALTHCARE AREA STATS------------')
printLine()
printLine()
print('The nearest hospitals from your given area are :')
for hospital in hospitals_stats.nearest_hospital_name:
    print('\t*** %s ***' % hospital)

print('\nThe distance to the nearest hospital from your given area is %.2f kilometers.\n'
                                                                % hospitals_stats.nearest_hospital_distance)

print('The average distance between the nearest hospitals to your given area is %.2f kilometers.\n'
                                                                                    % hospitals_stats.average_distance)
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------START COMPUTING REVIEWS STATS FOR AREA----------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
reviews_stats = ReviewsStats()
reviews_stats.computeReviews(reviews_stats.getJsonRequest(reviews_stats.getReviewsURL(userLatitude, userLongitude)))
reviews_stats.computeAverageReviewAndRating()
#-----------------------------------------------------------------------------------------------------------------------
#----------------------------------PRINT PEOPLE REVIEWS STATISTICS FOR USER GIVEN AREA----------------------------------
#-----------------------------------------------------------------------------------------------------------------------
printLine()
printLine()
print('---------------YOUR SELECTED AREA REVIEWS STATS-------------')
printLine()
printLine()
print('The total number of reviews collected from your given area is %i.' % reviews_stats.number_of_reviews)
print('The average rating given by other people on the area is %.1f.\n' % reviews_stats.rating_people_review)
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#----------------------------------------PRINT OVERALL RATINGS OF USER GIVEN AREA---------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
printLine()
printLine()
print('Safety Rating: \t\t%.1f/5.0' % police_stats.rating_safety)
print('Healthcare Rating: \t%.1f/5.0' % hospitals_stats.rating_health)
print('Reviews Rating: \t%.1f/5.0' % reviews_stats.rating_people_review)
print('-----------------\t-------')
rating_overall = (police_stats.rating_safety + hospitals_stats.rating_health + reviews_stats.rating_people_review) / 3
print('Overall Rating: \t%.1f/5.0' % rating_overall)
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------