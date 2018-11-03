from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
	    template = loader.get_template('carioquinha/index.html')
	    context = {
	    	'ola': "OI"
	    }

	    return render(request, 'carioquinha/index.html')