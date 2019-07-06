from django.http import HttpResponse

import requests
import logging
logger = logging.getLogger('pixels')

def index(request):
  return HttpResponse("Hello, world. You're at the pixels index.")

def show_image(request):
  # get all the info from the request
  if request.META['HTTP_USER_AGENT'] is None:
    ip = request.META['HTTP_USER_AGENT']
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