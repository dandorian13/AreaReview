from django.shortcuts import render
from django.http import *
from .area_review import *
from .templates.area_rev import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'area_rev/home.html')


@csrf_exempt
def result(request):
    if(request.method == 'POST'):
            datafromclient = request.POST['mydata']
            #just to test i only got one data from the area review class (police stats) to print it on the client screen.
            #also, when i have to restart the server every time i need to make a request because the second time when i
            #request something It gives me an index out of range error in police stats class with the line number.
            #so u might wanna check and correct that part as well.
            finalRes = runAreaReview(datafromclient)
            return HttpResponse(finalRes)








