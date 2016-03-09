from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

# Create views here.
def index(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request))

def questionnaire(request):
    return render_to_response('questionnaire.html',
                              context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html',
                              context_instance=RequestContext(request))
