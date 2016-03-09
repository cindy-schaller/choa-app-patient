from django.shortcuts import render
from django.http import HttpResponse

# Create views here.
def index(request):
    return HttpResponse("This screen will allow you to select a patient.")

def questionnaire(request):
    return HttpResponse("This screen will allow you to view and reply to the questionnaire.")

def about(request):
    return HttpResponse("A project of the Frogs' Greatest HITs team at Georgia Institute of Technology, Atlanta, GA.")
