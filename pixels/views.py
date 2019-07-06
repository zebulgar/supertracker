from django.http import HttpResponse
from django.template import RequestContext, Template, Context
from django.shortcuts import render

from django.utils import timezone
from pixels.models import Requests

import requests
import logging
import xmltodict

logger = logging.getLogger('pixels')

def index(request):
  return render(request, "index.html")

def pixel(request):
  username = request.GET.get('username','')
  pixel = request.GET.get('pixel','')

  requests = Requests.objects.filter(username=username)
  logger.error(requests)

  return render(request, "pixel.html",{'username': username, 'pixel': pixel, 'requests': requests})

def show_image(request):
  # get all the info from the request

  if 'HTTP_X_FORWARDED_FOR' in request.META.keys() and request.META['HTTP_X_FORWARDED_FOR'] is not None:
    ip = request.META['HTTP_X_FORWARDED_FOR']
  else:
    ip = ''

  # logger.error("I THINK THE IP IS")
  # logger.error(ip)
  # logger.error("AFTER")

  ipstack_url = "http://api.geoiplookup.net/?query=" + ip
  # logger.error("IP URL")
  # logger.error(ipstack_url)

  ip_info = requests.get(ipstack_url)

  json_info = xmltodict.parse(ip_info.content)

  # logger.error("IP INFO")
  logger.error(json_info)

  # get all the info VERY inefficiently
  if 'ip' in json_info.keys():
    ip = json_info['ip']
    if 'results' in ip.keys():
      results = ip['results']
      if 'result' in results.keys():
        result = results['result']
        if 'countryname' in result.keys():
          countryname = result['countryname']
        else:
          countryname = ''
        if 'city' in result.keys():
          city = result['city']
        else:
          city = ''
        if 'latitude' in result.keys():
          latitude = result['latitude']
        else:
          latitude = ''
        if 'longitude' in result.keys():
          longitude = result['longitude']
        else:
          longitude = ''    
        if 'isp' in result.keys():
          isp = result['isp']
        else:
          isp = ''

  # logger.error(request.META['HTTP_USER_AGENT'])
  # logger.error(request.META['HTTP_X_FORWARDED_FOR'])
  # ogger.error(request.META)

  username = request.GET.get('username','')
  pixel = request.GET.get('pixel','')

  # STORE THE REQUEST INFO
  r = Requests(username=username, isp=isp, city=city, country_name=countryname, latitude=latitude, longitude=longitude, time_opened=timezone.now())
  r.save()

  if pixel == 'pikachu':
    # return the pikachu image
    url='http://delian.io/pikachu.png'
  elif pixel == 'spyglass':
    logger.error("SPYGLASS BEFORE")
    url='http://delian.io/spyglass.png'
  elif pixel == 'transparent_pixel':
    url='http://delian.io/transparent_pixel.png'
  else:
    # default to pikachu!
    url='http://delian.io/pikachu.png'

  r = requests.get(url)
  return HttpResponse(r.content, content_type="image/png")