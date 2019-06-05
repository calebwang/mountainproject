import re

from util.cache import Cache, WeekCache
from util.util import map_chunk, paginate
from resources.resource import Resource 
from models.route import Route

CACHE_FILE = "cache.json"

class RouteCache(Cache):
  """
  Here, we assume the structure of the cache is from route_id to routes,
  and route_ids are ints (but are serialized as strings in the underlying FileCache)
  """
  def __init__(self, cache_file):
    super().__init__()
    self.cache = WeekCache(cache_file)

  def __contains__(self, key):
    return str(key) in self.cache

  def get(self, key):
    return self.cache.get(str(key))

  def put(self, key, value):
    self.cache.put(str(key), value)

  def flush(self):
    self.cache.flush()

  def keys(self):
    return map(int, self.cache.keys())

  def items(self):
    return [
      (int(key), value) for key, value in self.cache.items()
    ]
    

class Routes(Resource):
  def __init__(self, client, cache_file=CACHE_FILE):
    super().__init__(client)
    self.cache = RouteCache(CACHE_FILE)

  def _get_batch(self, route_ids):
    if not route_ids:
      return []
    data = self.client.get("get-routes", {
      "routeIds": ",".join(route_ids)
    })
    return data["routes"]

  def _get_batch_with_caching(self, route_ids):
    cached_routes = [
      route
      for route_id, route in self.cache.items()
      if route_id in route_ids
    ]

    uncached_route_ids = list(set(route_ids) - set(self.cache.keys()))
    fresh_routes = self._get_batch(uncached_route_ids)
    for route in fresh_routes:
      self.cache.put(route["id"], route)
    self.cache.flush()

    # Sort results by original request index
    return sorted(
      fresh_routes + cached_routes,
      key=lambda r: route_ids.index(r["id"])
    )

  def get_all(self, route_ids):
    request_limit=200
    return [
      Route(r) for r in 
      map_chunk(route_ids, request_limit, self._get_batch_with_caching)
    ]

  def get(self, route_id):
    return self.get_all([route_id])[0] 

  def _get_todos_page(self, email, start_pos):
    result = self.client.get("get-to-dos", {
      "email": email
    })
    todo_route_ids = result["toDos"]
    return self.client.routes.get_all(todo_route_ids)

  # Get all todos by default
  def get_todos(self, email, n=float("inf")):
    page_limit = 200
    return paginate(
      lambda start_pos: self._get_todos_page(email, start_pos),
      page_limit,
      n
    )

 

