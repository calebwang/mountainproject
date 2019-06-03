import json
import os

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


