import requests
class ReviewsStats:

#=======================================================================================================================
    def __new__(cls):
        return super(ReviewsStats, cls).__new__(cls)
#=======================================================================================================================
    def __init__(self):
        self.average_review = 0
        self.number_of_reviews = 0
        self.reviews_array = []
        self.reviewsURL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
        self.rating_people_review = 0
        self.peopleReviewsKEY = 'AIzaSyBdGqqScqrz_KKxCPeTEjWOcxW5bbYYwXY'

#=======================================================================================================================
    def getJsonRequest(self, someURL):
        getRequestResult = requests.get(someURL)
        getRequestResult = getRequestResult.json()
        return getRequestResult
#=======================================================================================================================
    def getReviewsURL(self, latitude, longitude):
        totalReviewsURL = self.reviewsURL + (str)(latitude) + ',' + (str)(longitude)
        totalReviewsURL = totalReviewsURL + '&radius=500&key=' + self.peopleReviewsKEY
        return totalReviewsURL
#=======================================================================================================================
    def computeReviews(self, reviewsJson):
        review_index = 0

        for review in reviewsJson['results']:
            if ('rating' in reviewsJson['results'][review_index]):
                self.reviews_array.append(reviewsJson['results'][review_index]['rating'])
            review_index += 1
#=======================================================================================================================
    def computeAverageReviewAndRating(self):
        self.number_of_reviews = len(self.reviews_array)
        sum_of_reviews = 0

        for review in self.reviews_array:
            sum_of_reviews += review

        self.average_review = sum_of_reviews / self.number_of_reviews
        self.average_review = float(str('%.1f' % self.average_review))
        self.rating_people_review = self.average_review
#=======================================================================================================================