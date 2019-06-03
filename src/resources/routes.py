import re

from util.cache import Cache
import util.util as util
from resources.resource import Resource 

CACHE_FILE = "cache.json"

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

  def __repr__(self):
    return "<Route name={} type={} grade={}>".format(self.name(), self.type(), self.grade())

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

class Routes(Resource):
  def __init__(self, client, cache_file=CACHE_FILE):
    super().__init__(client)
    self.cache = RouteCache(CACHE_FILE)

  def _get(self, route_ids):
    if not route_ids:
      return []
    data = self.client.get("get-routes", {
      "routeIds": ",".join(
        str(id) for id in route_ids
      )
    })
    return data["routes"]

  def _get_with_caching(self, route_ids):
    cached_routes = [
      route
      for route_id, route in self.cache.items()
      if route_id in route_ids
    ]

    uncached_route_ids = list(set(route_ids) - set(self.cache.keys()))
    fresh_routes = self._get(uncached_route_ids)
    for route in fresh_routes:
      self.cache.put(route["id"], route)
    self.cache.flush()

    # Sort results by original request index
    return sorted(
      fresh_routes + cached_routes,
      key=lambda r: route_ids.index(r["id"])
    )

  def get(self, route_ids):
    request_limit=100
    return [
      Route(r) for r in 
      util.map_chunk(route_ids, request_limit, self._get_with_caching)
    ]
 

