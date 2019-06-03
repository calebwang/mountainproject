import re

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


