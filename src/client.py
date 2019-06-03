import requests
import json

import resources.routes as routes
import resources.ticks as ticks

KEY = ""

RESOURCES = {
  "ticks": ticks.Ticks,
  "routes": routes.Routes
}

class Client(object):
  BASE_URL = "https://www.mountainproject.com/data"

  def __init__(self, key=KEY):
    self.key = key
    for key, resource in RESOURCES.items():
      setattr(self, key, resource(self))

  def get(self, endpoint, args):
    if "key" not in args:
      args["key"] = self.key

    arglist = [
      "{}={}".format(argname, value) 
      for argname, value in args.items()
    ]
    argstring = "&".join(arglist)
    url = "{}/{}?{}".format(
      Client.BASE_URL,
      endpoint,
      argstring 
    )
    response = requests.get(url)
    data = json.loads(response.content.decode("utf-8"))
    if data["success"] is not 1:
      raise Exception("request failed")
    return data
   
