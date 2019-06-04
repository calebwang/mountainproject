from resources.resource import Resource
from objects.tick import Tick

class Ticks(Resource):
  def get(self, email):
    result = self.client.get("get-ticks", {
      "email": email
    })
    return [
      Tick(t) for t in  result["ticks"]
    ]

