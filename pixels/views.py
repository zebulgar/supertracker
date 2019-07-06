from django.http import HttpResponse
from django.template import RequestContext, Template, Context
from django.shortcuts import render

import requests
import logging
logger = logging.getLogger('pixels')

def index(request):
  return render(request, "index.html")

def show_image(request):
  # get all the info from the request
	
  logger.error("I THINK THE IP IS")
  logger.error(request.META['HTTP_X_FORWARDED_FOR'])
  logger.error("AFTER")

  if request.META['HTTP_X_FORWARDED_FOR'] is not None:
    ip = request.META['HTTP_X_FORWARDED_FOR']
  else:
    ip = ''

  ipstack_url = "http://api.geoiplookup.net/?query=" + ip
  logger.error("IP URL")
  logger.error(ipstack_url)

  ip_info = requests.get(ipstack_url)

  logger.error("IP INFO")
  logger.error(ip_info.content)
  logger.error(request.META['HTTP_USER_AGENT'])
  # logger.error(request.META['HTTP_X_FORWARDED_FOR'])
  logger.error(request.META)

  # return the pikachu image
  url='https://icon2.kisspng.com/20171220/pke/pikachu-png-5a3a8ca037eb27.8436492915137865282291.jpg'
  r = requests.get(url)
  return HttpResponse(r.content, content_type="image/png")
