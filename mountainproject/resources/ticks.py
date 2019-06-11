import itertools

from mountainproject.resources.resource import Resource
from mountainproject.models.tick import Tick
from mountainproject.util.util import paginate

class Ticks(Resource):
  def _get_page(self, params, start_pos):
    result = self.client.get("get-ticks", params)
    ticks = [
      Tick(t, self.client) for t in result["ticks"]
    ]
    # Caching optimization, batch load all the relevant routes
    self.client.routes.get_all([tick.route_id for tick in ticks])
    return ticks

  # Get all ticks by default
  def get(self, user_id, n=float("inf")):
    page_limit = 200      
    params = { "userId": user_id }
    return paginate(
      lambda start_pos: self._get_page(params, start_pos),
      page_limit,
      n
    )

  # Get all ticks by default
  def get_by_email(self, email, n=float("inf")):
    page_limit = 200      
    params = { "email": email }
    return paginate(
      lambda start_pos: self._get_page(params, start_pos),
      page_limit,
      n
    )

