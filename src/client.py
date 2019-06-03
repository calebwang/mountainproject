import requests
import json
import os

import resources.routes as routes
import resources.ticks as ticks

RESOURCES = {
  "ticks": ticks.Ticks,
  "routes": routes.Routes
}

KEYFILE = "mp_key"
if os.path.exists(KEYFILE):
  with open(KEYFILE) as f:
    KEY=f.read().strip("\n")

class Client(object):
  BASE_URL = "https://www.mountainproject.com/data"

  def __init__(self, key=KEY):
    self.key = key
    for key, resource in RESOURCES.items():
      setattr(self, key, resource(self))

  def get(self, endpoint, params):
    if "key" not in args:
      params["key"] = self.key

    url = "{}/{}".format(
      Client.BASE_URL,
      endpoint
    )

    response = requests.get(url, params=params)
    data = json.loads(response.text)
    if data["success"] is not 1:
      raise Exception("request failed")
    return data
   
