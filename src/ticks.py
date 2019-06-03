import datetime

from clientresource import ClientResource

class Tick(object):
  def __init__(self, data):
    self.data = data

  def route_id(self):
    return self.data["routeId"]

  def style(self):
    return self.data["style"] or self.data["leadStyle"]

  def date(self):
    return datetime.datetime.strptime(self.data["date"], "%Y-%m-%d")

  def is_send(self, routes):
    # TODO: get route data, check type
    pass

class Ticks(ClientResource):
  def get(self, email):
    result = self.client.get("get-ticks", {
      "email": email
    })
    return [
      Tick(t) for t in  result["ticks"]
    ]

