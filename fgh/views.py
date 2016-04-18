from django.shortcuts import render,render_to_response,redirect
from django.template import RequestContext

# Create your views here.

def low_range_image(request):
    return render_to_response('low_range_image.html',
                              context_instance=RequestContext(request))

def high_range_image(request):
    return render_to_response('high_range_image.html',
                              context_instance=RequestContext(request))