import itertools

from resources.resource import Resource
from models.tick import Tick

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

    def page_generator():
      start_pos = 0
      num_results = 0
      while True:
        page = self._get_page(email, start_pos)
        yield page

        num_results += len(page)
        start_pos += 200

        if num_results >= n or len(page) < page_limit:
          return
  
    return list(itertools.chain.from_iterable(page_generator()))
    
