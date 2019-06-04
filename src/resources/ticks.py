import itertools

from resources.resource import Resource
from models.tick import Tick

class Ticks(Resource):
  def _get_page(self, email, start_pos):
    result = self.client.get("get-ticks", {
      "email": email
    })
    return [
      Tick(t) for t in  result["ticks"]
    ]

  def get(self, email, n=200):
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
    
