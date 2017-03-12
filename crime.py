import requests
import urllib.request
import json
#---------------------------------------- T H E - U S E D - U R L (APIs) -----------------------------------------------

geoURL = 'https://maps.googleapis.com/maps/api/geocode/json?address='
geoURL2 = '&key=AIzaSyBiUDxadU70wXZHE8e9dNYbdWmYSO4eHkI'
crime1 =  'https://data.police.uk/api/crimes-street/all-crime?'

#------------------------------------------ D E F I N E - F U N C T I O N S - H E R E-----------------------------------

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
a = []
k = 0
for i in result:
    a.append(result[k]['category'])
    k += 1
#-----------------------------------------------------------------------------------------------------------------------
# k = 0            # array A CONTAINS ALL THE TYPES OF CRIMES IN THAT AREA. TESTED AND IT WORKS
# for e in a:
#     print((a[k]))
#     k += 1
#     print('\n')
#-----------------------------------------------------------------------------------------------------------------------
word_counter = {}
for word in a:
    if word in word_counter:
        word_counter[word] += 1
    else:
        word_counter[word] = 1
secondBest = 0
highest = 0
for i in word_counter:
    if(word_counter[i] > secondBest):
        if(word_counter[i] > highest):
             highest = word_counter[i]
             highestCrime = i
        else:
            secondBest = word_counter[i]
            secondCrime = i
#------------------- P R I N T - T H E - S T A T S ---------------------------------------------------------------------
printLine()
print('T H E - S T A T S')
print('The total number of crimes : ', len(a))
print('The most frequest crime happening in your area is : ', highestCrime)
print('The most frequest crime happening in your area is : ', secondCrime)
printLine()
#===================================== C R I M E - S T A T S - O V E R =================================================
#check_to_branch