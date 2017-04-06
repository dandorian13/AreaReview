from django.shortcuts import render
from django.http import *
from .area_review import *
from .templates.area_rev import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

def home(request):

    # # form = post_code_form()
    # if(request.method == 'POST'):
    #     postCode = request.POST['address']
    #     # runAreaReview(postCode)
    #     print("The post code is : " , postCode)
    #     # return result(postCode)
    test = 4
    return render(request, 'area_rev/home.html')


@csrf_exempt
def result(request):
    if(request.method == 'POST'):
            datafromclient = request.POST['mydata']
            print(datafromclient)
            finalRes = runAreaReview(datafromclient)
            return HttpResponse(finalRes)








