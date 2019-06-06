import json
import os
import time

class Cache(object):
  def __init__(self):
    self.cache = dict()

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

class FileCache(Cache):
  def __init__(self, cache_file):
    super().__init__()
    self.cache_file = cache_file
    if os.path.exists(self.cache_file):
      with open(self.cache_file) as f:
        self.cache = json.load(f) 

  def flush(self):
    with open(self.cache_file, "w") as f:
      json.dump(self.cache, f)


class WeekCache(FileCache):
  """
  FileCache that evicts entries older than a week old.
  Instead of value, stores key => { timestamp: ts, value: value }
  and exposes the underlying key => value to users.
  """
  SECONDS_PER_WEEK = 60 * 60 * 24 * 7

  def __init__(self, cache_file):
    super().__init__(cache_file)
    self._evict()

  def _evict(self):
    now = int(time.time())
    self.cache = {
      key: entry 
      for key, entry in self.cache.items()
      if entry["timestamp"] > now - WeekCache.SECONDS_PER_WEEK
    }

  def get(self, key):
    entry = super().get(key)
    if entry:
      return entry["value"]

  def put(self, key, value):
      super().put(key, {
        "timestamp": int(time.time()),
        "value": value
      }) 

  def items(self):
    return [
      (key, value["value"]) for key, value in super().items()
    ]

  def values(self):
    return [
      value["value"]
      for value in super().values()
    ]

  
