import itertools

from mountainproject.resources.resource import Resource
from mountainproject.models.tick import Tick
from util.util import paginate

class Ticks(Resource):
  def _get_page(self, email, start_pos):
    result = self.client.get("get-ticks", {
      "email": email
    })
    ticks = [
      Tick(t, self.client) for t in result["ticks"]
    ]
    # Caching optimization, batch load all the relevant routes
    self.client.routes.get_all([tick.route_id for tick in ticks])
    return ticks

  # Get all ticks by default
  def get(self, email, n=float("inf")):
    page_limit = 200      
    return paginate(
      lambda start_pos: self._get_page(email, start_pos),
      page_limit,
      n
    )

