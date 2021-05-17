from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Links

# Create your views here.

def index(request):
    linklist = Links.objects.all()
    return render(request, 'search/index.html',{'linklist':linklist})