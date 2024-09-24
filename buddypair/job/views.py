# views.py
from django.http import HttpResponse

def hh(request):
    return HttpResponse("Hello, this is a test response!")
