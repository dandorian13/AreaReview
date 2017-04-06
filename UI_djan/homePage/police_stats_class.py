import requests
class PoliceStats:

#=======================================================================================================================
    def __new__(cls):
        return super(PoliceStats, cls).__new__(cls)
#=======================================================================================================================
    def __init__(self):
        self.policeURL = 'https://data.police.uk/api/crimes-street/all-crime?'
        self.rating_safety = 0
        self.number_of_crimes = 0
        self.crimes_array = []
        self.crime_outcomes = []
        self.category_counter = {}
        self.most_common_crime_number = 0
        self.second_most_common_crime_number = 0
        self.most_common_crime = ''
        self.second_most_common_crime = ''
        self.no_suspects_found = 0
        self.under_investigation = 0
        self.ratio_unsolved_crimes = 0
        self.ratio_investigating_crimes = 0
        self.ratio_solved_crimes = 0


    def getJsonRequest(self, someURL):
        getRequestResult = requests.get(someURL)
        getRequestResult = getRequestResult.json()
        return getRequestResult
#=======================================================================================================================
    def getPoliceURL(self, latitude, longitude):
        totalPoliceURL = self.policeURL + 'lat=' + str(latitude) + '&lng=' + str(longitude)
        return totalPoliceURL
#=======================================================================================================================
    def computeCrimesStats(self, policeJson):
        for crime in policeJson:
            self.crimes_array.append(policeJson[self.number_of_crimes]['category'])
            self.crime_outcomes.append(policeJson[self.number_of_crimes]['outcome_status'])
            self.number_of_crimes += 1
#=======================================================================================================================
    def countCrimeCategory(self):
        for crime_category in self.crimes_array:
            if crime_category in self.category_counter:
                self.category_counter[crime_category] += 1
            else:
                self.category_counter[crime_category] = 1
#=======================================================================================================================
    def computeMostCommonCrimes(self):
        for category in self.category_counter:
            if (self.category_counter[category] > self.most_common_crime_number):
                self.second_most_common_crime = self.most_common_crime
                self.second_most_common_crime_number = self.most_common_crime_number
                self.most_common_crime_number = self.category_counter[category]
                self.most_common_crime = category

            elif (self.category_counter[category] > self.second_most_common_crime_number):
                self.second_most_common_crime_number = self.category_counter[category]
                self.second_most_common_crime = category

        self.most_common_crime = self.most_common_crime.replace('-', ' ')
        self.second_most_common_crime = self.second_most_common_crime.replace('-', ' ')
#=======================================================================================================================
    def computeNumberOfCrimes(self):
        self.number_of_crimes = len(self.crimes_array)
#=======================================================================================================================
    def computeUnsolvedCrimes(self):
        for outcome in self.crime_outcomes:
            if 'no suspect' in str(outcome):
                self.no_suspects_found += 1
            if 'Under investigation' in str(outcome):
                self.under_investigation += 1
#=======================================================================================================================
    def computeCrimesRatios(self):
        self.ratio_unsolved_crimes = self.no_suspects_found / self.number_of_crimes * 100
        self.ratio_investigating_crimes = self.under_investigation / self.number_of_crimes * 100
        self.ratio_solved_crimes = 100 - self.ratio_unsolved_crimes - self.ratio_investigating_crimes
#=======================================================================================================================
    def computeSafetyRating(self):
        self.rating_safety = int(self.ratio_solved_crimes)
        self.rating_safety = self.rating_safety / 10
        self.rating_safety = self.rating_safety + self.ratio_investigating_crimes / 100
        self.rating_safety = self.rating_safety - self.ratio_unsolved_crimes / 100
        self.rating_safety = float(str('%.1f' % self.rating_safety))

        if (self.rating_safety > 5):
            self.rating_safety = 5
        if (self.rating_safety < 0):
            self.rating_safety = 0
#=======================================================================================================================