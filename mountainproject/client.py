import requests
import json
import os

from mountainproject.resources.routes import Routes
from mountainproject.resources.ticks import Ticks
from mountainproject.resources.users import Users

RESOURCES = {
  "ticks": Ticks,
  "routes": Routes,
  "users": Users
}

KEYFILE = "/tmp/mountainproject/mp_key"
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
    if "key" not in params:
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
   
