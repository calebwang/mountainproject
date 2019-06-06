import re
import enum

import mountainproject.models.grade 

class RouteType(enum.Enum):
  Trad = 1
  Sport = 2
  Boulder = 3
  TR = 4

  @staticmethod
  def from_string(type_string):
    # Prefer types in following order to resolve to a single type
    # Trad > Sport > Boulder > TR
    ranking = ["Trad", "Sport", "Boulder", "TR"]
    types = [
      t.strip() for t in
      type_string.split(",")
    ]
    primary_type = sorted(
      types,
      key=lambda t: ranking.index(t)
    )[0]
    for route_type in RouteType:
      if route_type.name == primary_type:
        return route_type
    return None

class Route(object):
  def __init__(self, data):
    self._data = data

  def __repr__(self):
    return "<\"{}\" type={} grade={}>".format(self.name, self.type, self.grade)

  @property
  def id(self):
    return self._data["id"]

  @property
  def name(self):
    return self._data["name"]

  @property
  def type(self):
    return RouteType.from_string(self._data["type"])

  @property
  def grade(self):
    return mountainproject.models.grade.Grade.from_string(self._data["rating"], self.type)


