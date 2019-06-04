import datetime

class Tick(object):
  def __init__(self, data):
    self.data = data

  def route_id(self):
    return self.data["routeId"]

  def route(self, routes):
    return routes.get([self.route_id()])[0]

  def style(self):
    return self.data["style"] or self.data["leadStyle"]

  def date(self):
    return datetime.datetime.strptime(self.data["date"], "%Y-%m-%d")

  def is_send(self, routes):
    # TODO: get route data, check type
    pass


