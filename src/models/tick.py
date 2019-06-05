import datetime

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
  def style(self):
    style = self._data["style"]
    leadStyle = self._data["leadStyle"]
    return "{}:{}".format(style, leadStyle) if leadStyle else style

  @property
  def date(self):
    return datetime.datetime.strptime(self._data["date"], "%Y-%m-%d")

  @property
  def is_send(self):
    # TODO: get route data, check type
    pass


