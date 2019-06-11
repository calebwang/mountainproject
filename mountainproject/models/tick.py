import enum
import datetime

from mountainproject.models.grade import Grade

class Tick(object):
  def __init__(self, data, client):
    self._data = data
    self._client = client

  def __repr__(self):
    return "<{} {}>".format(self.style, self.route)

  @property
  def route_id(self):
    return self._data["routeId"]

  @property
  def route(self):
    return self._client.routes.get(self.route_id)

  @property
  def route_type(self):
    return self.route.type

  @property
  def grade(self):
    return Grade.from_string(self._data["userRating"]) if self._data["userRating"] else self.route.grade

  @property
  def style(self):
    style = self._data["style"]
    leadStyle = self._data["leadStyle"]
    return leadStyle or style

  @property
  def date(self):
    return datetime.datetime.strptime(self._data["date"], "%Y-%m-%d").date()

