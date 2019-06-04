import datetime

class Tick(object):
  def __init__(self, data, routes):
    self.data = data
    self.routes = routes

  def __repr__(self):
    return "<{} \"{}\">".format(self.style(), self.route().name())

  def route_id(self):
    return self.data["routeId"]

  def route(self):
    return self.routes.get([self.route_id()])[0]

  def style(self):
    style = self.data["style"]
    leadStyle = self.data["leadStyle"]
    return "{}:{}".format(style, leadStyle) if leadStyle else style

  def date(self):
    return datetime.datetime.strptime(self.data["date"], "%Y-%m-%d")

  def is_send(self):
    # TODO: get route data, check type
    pass


