import requests
import json
import itertools
import os

import util

KEY=""
CACHE_FILE = "cache.json"

class Cache(object):
  def __init__(self, cache_file):
    self.cache_file = cache_file
    self.cache = dict()
    if os.path.exists(self.cache_file):
      with open(self.cache_file) as f:
        self.cache = json.load(f) 

  def get(self, key):
    return self.cache[key] if key in self.cache else None

  def put(self, key, value):
    self.cache[key] = value

  def flush(self, key, value):
    with open(self.cache_file, "w") as f:
      json.dump(self.cache, f)

class Api(object):
  BASE_URL = "https://www.mountainproject.com/data"
  def __init__(self, key=KEY, cache_file=CACHE_FILE):
    self.key = key
    self.cache = Cache(cache_file)

  def _get(self, endpoint, args):
    if "key" not in args:
      args["key"] = self.key
    arglist = [
      "{}={}".format(argname, value) 
      for argname, value in args.items()
    ]
    argstring = "&".join(arglist)
    response = requests.get(
      "{}/{}?{}".format(
        Api.BASE_URL,
        endpoint,
        argstring 
      )
    )
    data = json.loads(response.content.decode("utf-8"))
    if data["success"] is not 1:
      raise Exception("request failed")
    return data
  
  def ticks(self, email):
    result = self._get("get-ticks", {
      "email": email
    })
    return result["ticks"]

  def _routes(self, route_ids):
    data = self._get("get-routes", {
      "routeIds": ",".join(
        str(id) for id in route_ids
      )
    })
    rtes = data["routes"] 
    for rte in rtes:
      self.cache.put(rte["id"], rte)
    self.cache.flush()
    return rtes

  def routes(self, route_ids):
    request_limit=100
    return util.map_chunk(route_ids, request_limit, self._routes)
    
    
