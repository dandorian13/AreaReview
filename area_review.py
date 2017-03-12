#google geo api : AIzaSyBiUDxadU70wXZHE8e9dNYbdWmYSO4eHkI
import requests
import urllib.request
import json
#-----------------------------------------------------------------------------------------------------------------------

geoURL = 'https://maps.googleapis.com/maps/api/geocode/json?address='
geoURL2 = '&key=AIzaSyBiUDxadU70wXZHE8e9dNYbdWmYSO4eHkI'
crime1 =  'https://data.police.uk/api/crimes-street/all-crime?'

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

if(date is ''):
    total_CrimeURL =  str(crime1) + 'lat=' + str(latitude) + '&lng=' + str(longitude)
else:
    total_CrimeURL = str(crime1) + 'lat=' + str(latitude) + '&lng=' + str(longitude) + \
                 '&date=' + str(date)

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

for outcome in crime_outcomes:
    if 'no suspect' in str(outcome):
        no_suspects += 1
    if 'Under investigation' in str(outcome):
        under_investigation += 1
#------------------- P R I N T - T H E - S T A T S ---------------------------------------------------------------------
printLine()
printLine()
print('------------------YOUR SELECTED AREA STATS------------------')
printLine()
printLine()
if highestCrime is not '':
    print('The total number of crimes in given area is %s.\n' % len(crime_array))
    print('The most frequest crime happening in your area is %s.\n' % highestCrime)
    #compute useful information
    ratio_unsolved = no_suspects / len(crime_array) * 100
    ratio_investigating = under_investigation / len(crime_array) * 100
    ###########################
    print('%.2f%%' % ratio_unsolved + ' of the total crimes finished without finding any suspect.\n')
    print('%.2f%%' % ratio_investigating, ' of the total crimes are still under investigation.')
else:
    print('No crimes could be found at given location')
printLine()
#===================================== C R I M E - S T A T S - O V E R =================================================