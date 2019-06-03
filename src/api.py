import requests
import json
import itertools
import re

import util 
from cache import RouteCache
from route import Route

KEY = ""
CACHE_FILE = "cache.json"

class Api(object):
  BASE_URL = "https://www.mountainproject.com/data"

  def __init__(self, key=KEY, cache_file=CACHE_FILE):
    self.key = key
    self.cache = RouteCache(cache_file)

  def _get(self, endpoint, args):
    if "key" not in args:
      args["key"] = self.key

    arglist = [
      "{}={}".format(argname, value) 
      for argname, value in args.items()
    ]
    argstring = "&".join(arglist)
    url = "{}/{}?{}".format(
      Api.BASE_URL,
      endpoint,
      argstring 
    )
    response = requests.get(url)
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
    if not route_ids:
      return []
    data = self._get("get-routes", {
      "routeIds": ",".join(
        str(id) for id in route_ids
      )
    })
    return data["routes"]

  def _routes_with_caching(self, route_ids):
    cached_routes = [
      route
      for route_id, route in self.cache.items()
      if route_id in route_ids
    ]

    uncached_route_ids = list(set(route_ids) - set(self.cache.keys()))
    fresh_routes = self._routes(uncached_route_ids)
    for route in fresh_routes:
      self.cache.put(route["id"], route)
    self.cache.flush()

    # Sort results by original request index
    return sorted(
      fresh_routes + cached_routes,
      key=lambda r: route_ids.index(r["id"])
    )

  def routes(self, route_ids):
    request_limit=100
    return [
      Route(r) for r in 
      util.map_chunk(route_ids, request_limit, self._routes_with_caching)
    ]
    
