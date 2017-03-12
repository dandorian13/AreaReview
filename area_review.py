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
    print('-----------------------------------------------------------------------------------------------------------')
#-------------------------- M A I N - S T A R T S - H E R E ------------------------------------------------------------
printLine()
print('Note: Date gives you the crime stats of that period. If ignored, gives you the crimes of the most recent\n\t' +
      '  period')

print('**\t  If you wish to ignore the date, just leave it blank(that is carriage return). Thank you\t**')
printLine()
date = input('Input the specific month and year YYYY/MM:')
date = forDate(date)
print(date)
address = input('Enter your address seperated by comas: ')
address = forAddress(address)
totalGeo = geoURL + address + geoURL2 #total complete URL
resultGeo = requests.get(totalGeo) #get the api request
resultGeo = resultGeo.json()
print(resultGeo)
location = resultGeo['results'][0]['geometry']['location']
latitude, longitude = location['lat'], location['lng'] #got the latitude and longitude from geo api
printLine()
printLine()
print (latitude, ' - ', longitude)
printLine()
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
for outcome in crime_outcomes:
    if 'no suspect' in str(outcome):
        no_suspects += 1
#------------------- P R I N T - T H E - S T A T S ---------------------------------------------------------------------
printLine()
print('T H E - S T A T S')
if highestCrime is not '':
    print('The total number of crimes : ', len(crime_array))
    print('The most frequest crime happening in your area is : ', highestCrime)
    ratio = no_suspects / len(crime_array) * 100
    print(ratio, '% of the total crimes finished without finding any suspect')
else:
    print('No crimes could be found at given location')
printLine()
#===================================== C R I M E - S T A T S - O V E R =================================================