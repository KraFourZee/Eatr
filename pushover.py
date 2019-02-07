import json
import http.client, urllib
from configparser import ConfigParser

# reading config file
parser = ConfigParser()
parser.read('configs/config.ini')

def sendText(msg):
  conn = http.client.HTTPSConnection("api.pushover.net:443")
  conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
      "token": parser.get('pushover', 'token'),
      "user": parser.get('pushover', 'user'),
      "message": msg,
    }), { "Content-type": "application/x-www-form-urlencoded" })
  conn.getresponse()