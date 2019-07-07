from django.http import HttpResponse
from django.template import RequestContext, Template, Context
from django.shortcuts import render

from django.utils import timezone

from pixels.models import Requests

import requests
import logging
import json
from ua_parser import user_agent_parser

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

  # if you are trying to shut me down, this is one of the more vulnerable parts, just fire off enough requests here:
  ipdata_url = "https://api.ipdata.co/"+ip+"?api-key=2426c12568210a843d3ac8e14d9933764e73f0d8e84fc92834314a58"
  # logger.error("IP URL")
  # logger.error(ipstack_url)

  ip_info = requests.get(ipdata_url)
  ip_content = json.loads(ip_info.content)
  # logger.error("IP INFO")
  logger.error(ip_content)

  logger.error("META")
  logger.error(request.META)

  client = ''
  os = ''
  device = ''

  if 'HTTP_USER_AGENT' in request.META.keys():
    ua_string = request.META['HTTP_USER_AGENT']
    parsed_string = user_agent_parser.Parse(ua_string)
    logger.error("PARSED USER AGENT")
    logger.error(parsed_string)
    if 'user_agent' in parsed_string.keys():
      agent_data = parsed_string['user_agent']
      if 'family' in agent_data.keys():
        client = agent_data['family']

    if 'os' in parsed_string.keys():
      os_data = parsed_string['os']
      if 'family' in os_data.keys():
        os = os_data['family']

    if 'device' in parsed_string.keys():
      device_data = parsed_string['device']
      if 'family' in device_data.keys():
        device = device_data['family']

  # get all the info VERY inefficiently

  if 'ip' in ip_content.keys():
    result = ip_content
    if 'region' in result.keys():
      region = result['region']
    else:
      region = ''
    if 'country_name' in result.keys():
      country_name = result['country_name']
    else:
      country_name = ''
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
    if 'organisation' in result.keys():
      isp = result['organisation']
    else:
      isp = ''

  # logger.error(request.META['HTTP_USER_AGENT'])
  # logger.error(request.META['HTTP_X_FORWARDED_FOR'])
  # ogger.error(request.META)

  username = request.GET.get('username','')
  pixel = request.GET.get('pixel','')

  # STORE THE REQUEST INFO
  r = Requests(username=username, isp=isp, client=client, os=os, device=device, city=city, region=region, country_name=country_name, latitude=latitude, longitude=longitude, time_opened=timezone.now())
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