from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from TwitterSearch import *
import requests

def twitterRequest(keywords):
	try:
		tso = TwitterSearchOrder() # create a TwitterSearchOrder object
		tso.set_keywords([keywords]) # let's define all words we would like to have a look for
		tso.set_include_entities(False) # and don't give us all those entity information

		# it's about time to create a TwitterSearch object with our secret tokens
		ts = TwitterSearch(
			consumer_key = 'zPfGDbJhCxkYMTunFMlJaROB9',
			consumer_secret = 'YC49zc34ZNaUJp3JfXO5RosMGOohRTs8xxSt2ISme5riTbJDAg',
			access_token = '1358282929-DQnLw1Vi8jwUzwseDsFPpTLZVJMCS4gWt0txfva',
			access_token_secret = 'jsoxXKvDf5481szlQ2dvoDGKvNE8yuu5tQ4AQ5gxVTTuK'
		 )
		result = ""
		 # this is where the fun actually starts :)
		for tweet in ts.search_tweets_iterable(tso):
			result += ( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) ) + "\n"
		return result
	except TwitterSearchException as e: # take care of all those ugly errors if there are some
		print(e)

def getTransitoTwittes():
	try:
		col = list(filter(lambda t: t.find("TWITTER ALERT") == -1, twitterRequest('@OperacoesRio').split("\n")))
		col = filter(lambda t: t.find("#PrimaveraCOR2018") == -1, col)
		col = filter(lambda t: t.find("FUTEBOL") == -1, col)
		col = filter(lambda t: t.find("CHAT COR") == -1, col)
		col = filter(lambda t: t.find("PRÓXIMOS DIAS") == -1, col)
		col = filter(lambda t: t.find("SMS") == -1, col)
		col = filter(lambda t: t.find("#RDRJ") == -1, col)   
		col = filter(lambda t: t.find("|") != -1, col)
		col = list(filter(lambda t: len(t) > 120, col))
	except Exception as e:
		return None

	return col

def getViolenciaTwittes():
	try:
		col = list(filter(lambda t: t.find("tweeted:") == -1, twitterRequest('@RJ_OTT').split("\n")))
		col = list(filter(lambda t: len(t) > 1, col))
		col2 = []

		for i in range(0, len(col), 2):
			col2.append(str(col[i]) + " " + str(col[i+1]))

		col = list(filter(lambda t: t.find("/") != -1, col2))
		col = list(filter(lambda t: t.find("@") == -1, col))
		col = list(filter(lambda t: t.find("#") == -1, col))
		col = list(filter(lambda t: t.find(" - ") != -1, col))
	except Exception as e:
		return None

	return col

def getEventosTwittes():
	try:
		col = list(filter(lambda t: len(t) > 120, twitterRequest('@Cultura_Rio').split("\n")))
	except Exception as e:
		return None

	return col


# Create your views here.
def index(request):
		template = loader.get_template('carioquinha/index.html')
		context = {
			'violenciaTwitter' :  getViolenciaTwittes(),
			'transitoTwitter' : getTransitoTwittes(),
			'eventoTwitter' : getEventosTwittes()
		}

		return render(request, 'carioquinha/index.html', context)
