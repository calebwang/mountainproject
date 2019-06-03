import requests
import json
import itertools
import os
import re

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

  def __getitem__(self, key):
    return self.get(key)

  def __setitem__(self, key, value):
    self.put(key, value)

  def get(self, key):
    return self.cache[key] if key in self.cache else None

  def put(self, key, value):
    self.cache[key] = value

  def items(self):
    return self.cache.items() 

  def keys(self):
    return self.cache.keys()

  def values(self):
    return self.cache.values()

  def flush(self):
    with open(self.cache_file, "w") as f:
      json.dump(self.cache, f)

class RouteCache(Cache):
  """
  Here, we assume the structure of the cache is from route_id to routes,
  and route_ids are ints (but are serialized as strings, thanks JSON)
  """
  def __init__(self, cache_file):
    super().__init__(cache_file)
    self.cache = {
      int(id): route for id, route in self.cache.items()
    }

class Route(object):
  def __init__(self, data):
    self.data = data

  def id(self):
    return self.data["id"]

  def name(self):
    return self.data["name"]

  def type(self):
    # Prefer types in following order to resolve to a single type
    # Trad > Sport > Boulder > TR
    ranking = ["Trad", "Sport", "Boulder", "TR"]
    types = [
      t.strip() for t in
      self.data["type"].split(",")
    ]
    return sorted(
      types,
      key=lambda t: ranking.index(t)
    )[0]

  def _extract_grade(self, regex):
    grades = self.data["rating"].split(" ")
    matching_grades = [
      m.group(0) for m in [
        re.match(regex, grade) for grade in grades
      ] if m is not None
    ]
    if matching_grades:
      return matching_grades[0]
    return None

  def _yds_grade(self):
    return self._extract_grade(r"5\.[0-9]+[abcd+-]?")

  def _v_grade(self):
    return self._extract_grade(r"V[0-9]+")

  def pg_grade(self):
    return self._extract_grade(r"X|R|PG-13")

  def grade(self):
    if self.type() == "Boulder":
      return self._v_grade()
    else:
      return self._yds_grade()

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
    
