from django.http import HttpResponse
from django.template import RequestContext, Template, Context
from django.shortcuts import render

import requests
import logging
logger = logging.getLogger('pixels')

def index(request):
  return render(request, "index.html")

def pixel(request):
  username = request.GET.get('username','')
  pixel = request.GET.get('pixel','')

  return render(request, "pixel.html",{'username': username, 'pixel': pixel})

def show_image(request):
  # get all the info from the request

  if 'HTTP_X_FORWARDED_FOR' in request.META.keys() and request.META['HTTP_X_FORWARDED_FOR'] is not None:
    ip = request.META['HTTP_X_FORWARDED_FOR']
  else:
    ip = ''

  logger.error("I THINK THE IP IS")
  logger.error(ip)
  logger.error("AFTER")

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
  url='http://www.pngmart.com/files/2/Pikachu-PNG-File.png'
  r = requests.get(url)
  return HttpResponse(r.content, content_type="image/png")
