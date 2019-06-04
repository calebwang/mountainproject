import re

from util.cache import WeekCache
import util.util as util
from resources.resource import Resource 
from models.route import Route

CACHE_FILE = "cache.json"

class RouteCache(WeekCache):
  """
  Here, we assume the structure of the cache is from route_id to routes,
  and route_ids are ints (but are serialized as strings, thanks JSON)
  """
  def __init__(self, cache_file):
    super().__init__(cache_file)
    self.cache = {
      int(id): route for id, route in self.cache.items()
    }

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
 

