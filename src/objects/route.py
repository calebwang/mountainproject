import re
import enum

import objects.rating 

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
    self.data = data

  def __repr__(self):
    return "<Route name=\"{}\" type={} grade={}>".format(self.name(), self.type(), self.grade())

  def id(self):
    return self.data["id"]

  def name(self):
    return self.data["name"]

  def type(self):
    return RouteType.from_string(self.data["type"])

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

  def grade(self):
    return objects.rating.Rating.from_string(self.data["rating"], self.type())


